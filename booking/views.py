from django.db.models import Q
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from decimal import Decimal

from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer
from vehicle.models import Vehicle, VehicleType
from useraccount.models import CustomUser, Address

# Custom permission classes


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow if admin or if the object belongs to the user
        return request.user.is_staff or obj.user == request.user


class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Booking.objects.all().order_by('-booking_date')


class UserBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users only see their own bookings
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')


class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    queryset = Booking.objects.all()


class BookingUpdateView(generics.UpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    queryset = Booking.objects.all()

    def perform_update(self, serializer):
        # Check if status is being changed to 'canceled'
        if 'status' in self.request.data and self.request.data['status'] == 'canceled':
            serializer.save(
                cancellation_time=timezone.now(),
                cancellation_reason=self.request.data.get(
                    'cancellation_reason', '')
            )
        else:
            serializer.save()


class BookingDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    queryset = Booking.objects.all()

    def perform_destroy(self, instance):
        # Instead of deleting, mark as canceled
        instance.status = 'canceled'
        instance.cancellation_time = timezone.now()
        instance.cancellation_reason = "Booking deleted by user"
        instance.save()


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def generate_booking_code(self):
        """Generate a unique booking code"""
        while True:
            code = get_random_string(
                length=10, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            if not Booking.objects.filter(booking_code=code).exists():
                return code

    def generate_qr_code(self, booking):
        """Generate QR code with booking information"""
        # Create QR code data
        qr_data = (
            f"BOOKING CODE: {booking.booking_code}\n"
            f"NAME: {booking.user.get_full_name()}\n"
            f"FROM: {booking.origin_address}\n"
            f"TO: {booking.destination_address}\n"
            f"DATE: {booking.travel_date.strftime('%Y-%m-%d %H:%M')}\n"
            f"VEHICLE: {booking.vehicle.make} {booking.vehicle.model}\n"
            f"TRIP TYPE: {dict(Booking.TRIP_TYPES).get(booking.trip_type)}\n"
            f"PASSENGERS: {booking.people}\n"
            f"LUGGAGE: {booking.luggage}\n"
            f"CONTACT: {booking.user.phone or 'N/A'}"
        )

        if booking.trip_type == 'RT' and booking.return_date:
            qr_data += f"\nRETURN DATE: {booking.return_date.strftime('%Y-%m-%d %H:%M')}"

        # Generate QR code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to Django ContentFile
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return ContentFile(buffer.getvalue(), name=f"booking_{booking.booking_code}.png")

    def validate_vehicle_availability(self, vehicle, travel_date, return_date=None, trip_type=None):
        """Check if vehicle is available for the requested dates"""
        # Check if the vehicle is available in general
        if not vehicle.is_available:
            raise ValidationError("This vehicle is not available for booking")

        # Check for conflicting bookings
        conflicting_bookings = Booking.objects.filter(
            vehicle=vehicle,
            status__in=['pending', 'confirmed'],
        ).exclude(
            status='canceled'
        )

        # For one-way or hourly/daily rentals
        if trip_type in ['OW', 'HR', 'DR']:
            # Check if there's a booking that overlaps with the travel date
            conflicts = conflicting_bookings.filter(
                travel_date__lte=travel_date +
                timedelta(hours=4),  # Allow 4-hour buffer
                actual_dropoff_time__isnull=True
            )
            if conflicts.exists():
                raise ValidationError(
                    "This vehicle is already booked for the selected date")

        # For round trips
        elif trip_type == 'RT' and return_date:
            # Check if there's a booking that overlaps with either travel date or return date
            conflicts = conflicting_bookings.filter(
                Q(travel_date__range=(travel_date, return_date)) |
                Q(return_date__range=(travel_date, return_date))
            )
            if conflicts.exists():
                raise ValidationError(
                    "This vehicle is already booked during your selected dates")

    def calculate_trip_cost(self, vehicle, trip_type, travel_date, return_date=None):
        """Calculate the cost of the trip based on vehicle rates and trip type"""
        cost = Decimal('0.00')

        if trip_type == 'HR':  # Hourly Rental
            if not vehicle.hourly_rate:
                raise ValidationError(
                    "This vehicle doesn't support hourly rentals")
            hours = 1  # Minimum 1 hour
            cost = vehicle.hourly_rate * hours

        elif trip_type == 'DR':  # Daily Rental
            if not vehicle.daily_rate:
                raise ValidationError(
                    "This vehicle doesn't support daily rentals")
            days = 1  # Minimum 1 day
            cost = vehicle.daily_rate * days

        elif trip_type == 'OW':  # One Way
            if not vehicle.daily_rate:
                raise ValidationError(
                    "Pricing information unavailable for this vehicle")
            cost = vehicle.daily_rate

        elif trip_type == 'RT':  # Round Trip
            if not vehicle.daily_rate or not return_date:
                raise ValidationError(
                    "Pricing or return date information missing")

            # Calculate days between travel_date and return_date
            days = (return_date - travel_date).days + 1
            if days < 1:
                days = 1
            cost = vehicle.daily_rate * Decimal(days)

        return cost

    @transaction.atomic
    def perform_create(self, serializer):
        # Get data from request
        vehicle_id = self.request.data.get('vehicle')
        trip_type = self.request.data.get('trip_type')
        travel_date = serializer.validated_data.get('travel_date')
        return_date = serializer.validated_data.get('return_date')

        # Get vehicle
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        # Check for special options
        if serializer.validated_data.get('with_entourage') and not vehicle.has_entourage_option:
            raise ValidationError(
                "This vehicle doesn't support entourage option")

        if serializer.validated_data.get('with_security') and not vehicle.has_security_option:
            raise ValidationError(
                "This vehicle doesn't support security option")

        # Check people count against vehicle capacity
        if serializer.validated_data.get('people', 0) > vehicle.total_seats:
            raise ValidationError(
                f"This vehicle can only accommodate {vehicle.total_seats} passengers")

        # Validate vehicle availability
        self.validate_vehicle_availability(
            vehicle, travel_date, return_date, trip_type)

        # Generate booking code
        booking_code = self.generate_booking_code()

        # Create booking
        booking = serializer.save(
            user=self.request.user,
            booking_code=booking_code,
            booking_date=timezone.now(),
            status='pending'
        )

        # Generate and save QR code
        qr_code_file = self.generate_qr_code(booking)
        booking.qr_code = qr_code_file
        booking.save()

        return booking

    def create(self, request, *args, **kwargs):
        # Get vehicle_id from query parameters if not in request data
        if 'vehicle' not in request.data and 'vehicle_id' in request.query_params:
            request.data['vehicle'] = request.query_params.get('vehicle_id')

        # If origin address is not provided, try to use user's address
        if not request.data.get('origin_address'):
            try:
                address = Address.objects.get(user=request.user)
                full_address = f"{address.street}, {address.city}, {address.state}"
                request.data['origin_address'] = full_address
            except Address.DoesNotExist:
                pass

        # If pickup_address is not provided, try to use user's address
        if not request.data.get('pickup_address'):
            try:
                address = Address.objects.get(user=request.user)
                full_address = f"{address.street}, {address.city}, {address.state}"
                request.data['pickup_address'] = full_address
            except Address.DoesNotExist:
                pass

        # Round trip validation
        if request.data.get('trip_type') == 'RT' and not request.data.get('return_date'):
            return Response(
                {"error": "Return date is required for round trips"},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            # Get the created booking
            booking = Booking.objects.get(id=response.data['id'])

            # Calculate and display estimated cost
            vehicle = booking.vehicle
            trip_type = booking.trip_type
            travel_date = booking.travel_date
            return_date = booking.return_date

            try:
                estimated_cost = self.calculate_trip_cost(
                    vehicle, trip_type, travel_date, return_date)

                # Add additional information to the response
                response.data['qr_code_url'] = request.build_absolute_uri(
                    booking.qr_code.url) if booking.qr_code else None
                response.data['estimated_cost'] = estimated_cost
                response.data['message'] = (
                    f"Booking created successfully! Your booking code is {booking.booking_code}. "
                    f"Estimated cost: ${estimated_cost}"
                )
            except Exception as e:
                response.data[
                    'message'] = f"Booking created successfully! Your booking code is {booking.booking_code}."

        return response
