from rest_framework import serializers
from .models import Booking
from useraccount.serializers import CustomUserSerializer
from vehicle.serializers import VehicleSerializer


class BookingSerializer(serializers.ModelSerializer):
    user_details = CustomUserSerializer(source='user', read_only=True)
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    booking_duration = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('booking_date', 'booking_code', 'qr_code',
                            'is_checked_in', 'is_checked_out',
                            'check_in_time', 'check_out_time')

    def get_booking_duration(self, obj):
        """Calculate booking duration in days or hours"""
        if obj.trip_type == 'RT' and obj.return_date:
            # Calculate days for round trip
            delta = obj.return_date - obj.travel_date
            return f"{delta.days} days"
        elif obj.trip_type in ['HR', 'DR']:
            # For hourly and daily rentals (estimate)
            return "Varies based on usage"
        else:
            return "One-way trip"

    def validate(self, data):
        # Check if return_date is provided for round trips
        if data.get('trip_type') == 'RT' and not data.get('return_date'):
            raise serializers.ValidationError(
                "Return date is required for round trips")

        # For round trips, make sure return date is after travel date
        if data.get('trip_type') == 'RT' and data.get('return_date') and data.get('travel_date'):
            if data['return_date'] <= data['travel_date']:
                raise serializers.ValidationError(
                    "Return date must be after travel date")

        # Validate capacity
        if data.get('people') and data.get('vehicle'):
            if data['people'] > data['vehicle'].total_seats:
                raise serializers.ValidationError(
                    f"This vehicle can only accommodate {data['vehicle'].total_seats} passengers")

        return data


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ('booking_date', 'booking_code', 'qr_code',
                   'is_checked_in', 'is_checked_out',
                   'check_in_time', 'check_out_time',
                   'actual_pickup_time', 'actual_dropoff_time',
                   'is_paid', 'cancellation_reason', 'cancellation_time',
                   'status')

    def validate(self, data):
        """Validate booking data"""
        # Make travel date is in the future
        from django.utils import timezone
        if data['travel_date'] <= timezone.now():
            raise serializers.ValidationError(
                "Travel date must be in the future")

        # Check if return_date is provided for round trips
        if data.get('trip_type') == 'RT' and not data.get('return_date'):
            raise serializers.ValidationError(
                "Return date is required for round trips")

        # For round trips, make sure return date is after travel date
        if data.get('trip_type') == 'RT' and data.get('return_date'):
            if data['return_date'] <= data['travel_date']:
                raise serializers.ValidationError(
                    "Return date must be after travel date")

        # Check vehicle capacity
        if 'people' in data and 'vehicle' in data:
            if data['people'] > data['vehicle'].total_seats:
                raise serializers.ValidationError(
                    f"This vehicle can only accommodate {data['vehicle'].total_seats} passengers")

        # Validate special options
        if data.get('with_entourage') and 'vehicle' in data:
            if not data['vehicle'].has_entourage_option:
                raise serializers.ValidationError(
                    "This vehicle doesn't support entourage option")

        if data.get('with_security') and 'vehicle' in data:
            if not data['vehicle'].has_security_option:
                raise serializers.ValidationError(
                    "This vehicle doesn't support security option")

        return data
