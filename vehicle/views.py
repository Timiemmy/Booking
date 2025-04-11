from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import generics, status
from django.db import transaction
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import VehicleType, Vehicle, Amenity, VehicleImage, VehicleLocation
from .serializers import (
    VehicleTypeSerializer,
    VehicleSerializer,
    AmenitySerializer,
    VehicleImageSerializer,
    VehicleImageCreateSerializer,
    #VehicleCreateSerializer
)
from .permissions import IsAuthenticatedOrReadAdmin


# VehicleType views
class VehicleTypeList(generics.ListCreateAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = [IsAuthenticatedOrReadAdmin]


class VehicleTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = [IsAuthenticatedOrReadAdmin]


# Amenity views
class AmenityList(generics.ListCreateAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [IsAuthenticatedOrReadAdmin]


class AmenityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [IsAuthenticatedOrReadAdmin]


# Vehicle views
class VehicleList(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'make', 'model',
                        'year', 'is_active', 'is_available']
    ordering_fields = ['make', 'model', 'year', 'departure_time']
    ordering = ['-departure_time']  # Default ordering - newest departure first

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by vehicle type if specified
        vehicle_type = self.request.query_params.get('vehicle_type')
        if vehicle_type:
            queryset = queryset.filter(category__id=vehicle_type)

        return queryset


'''
class VehicleCreate(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Extract images data from the request
        images_data = request.data.pop('images', [])

        # Create vehicle first
        vehicle_serializer = self.get_serializer(data=request.data)
        vehicle_serializer.is_valid(raise_exception=True)
        vehicle = vehicle_serializer.save()

        # Process and create each image
        images = []
        for image_data in images_data:
            # If image_data is a dict with image file and other fields
            if isinstance(image_data, dict):
                image_data['vehicle'] = vehicle.id
                image_serializer = VehicleImageSerializer(data=image_data)
                image_serializer.is_valid(raise_exception=True)
                image = image_serializer.save()
                images.append(image_serializer.data)
            # If only image files are provided
            else:
                image = VehicleImage.objects.create(
                    vehicle=vehicle,
                    image=image_data
                )
                images.append(VehicleImageSerializer(image).data)

        # Return combined response
        response_data = vehicle_serializer.data
        response_data['images'] = images

        return Response(response_data, status=status.HTTP_201_CREATED)
'''


class VehicleCreateWithImages(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Extract images data
        images_data = []
        for key, value in request.data.items():
            if key.startswith('images[') and key.endswith('][image]'):
                index = key[7:-8]  # Extract index from 'images[0][image]'

                # Find corresponding caption if exists
                caption_key = f'images[{index}][caption]'
                caption = request.data.get(caption_key, '')

                images_data.append({
                    'image': value,
                    'caption': caption
                })

        # Handle regular vehicle data
        vehicle_data = {}
        for key, value in request.data.items():
            if not key.startswith('images['):
                vehicle_data[key] = value

        # Create vehicle
        vehicle_serializer = self.get_serializer(data=vehicle_data)
        vehicle_serializer.is_valid(raise_exception=True)
        vehicle = vehicle_serializer.save()

        # Create images
        for image_data in images_data:
            image_serializer = VehicleImageCreateSerializer(data=image_data)
            if image_serializer.is_valid():
                image_serializer.save(vehicle=vehicle)

        headers = self.get_success_headers(vehicle_serializer.data)
        return Response(vehicle_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VehicleUpdateWithImages(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        vehicle = self.get_object()

        # Extract images data
        images_data = []
        for key, value in request.data.items():
            if key.startswith('images[') and key.endswith('][image]'):
                index = key[7:-8]  # Extract index from 'images[0][image]'

                # Find corresponding caption if exists
                caption_key = f'images[{index}][caption]'
                caption = request.data.get(caption_key, '')

                # Check if there's an image ID (for existing images)
                id_key = f'images[{index}][id]'
                image_id = request.data.get(id_key, None)

                images_data.append({
                    'id': image_id,
                    'image': value,
                    'caption': caption
                })

        # Handle regular vehicle data
        vehicle_data = {}
        for key, value in request.data.items():
            if not key.startswith('images['):
                vehicle_data[key] = value

        # Update vehicle
        vehicle_serializer = self.get_serializer(
            vehicle, data=vehicle_data, partial=True)
        vehicle_serializer.is_valid(raise_exception=True)
        vehicle = vehicle_serializer.save()

        # Process images
        for image_data in images_data:
            image_id = image_data.pop('id', None)

            if image_id:
                # Update existing image
                try:
                    vehicle_image = VehicleImage.objects.get(
                        id=image_id, vehicle=vehicle)
                    image_serializer = VehicleImageCreateSerializer(
                        vehicle_image, data=image_data, partial=True)
                    if image_serializer.is_valid():
                        image_serializer.save()
                except VehicleImage.DoesNotExist:
                    pass
            else:
                # Create new image
                image_serializer = VehicleImageCreateSerializer(
                    data=image_data)
                if image_serializer.is_valid():
                    image_serializer.save(vehicle=vehicle)

        # Handle image deletions
        if 'delete_images' in request.data:
            delete_ids = request.data.getlist('delete_images')
            VehicleImage.objects.filter(
                id__in=delete_ids, vehicle=vehicle).delete()

        return Response(vehicle_serializer.data)


# Vehicle image upload for existing vehicle
class VehicleImageUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    def post(self, request, vehicle_id, format=None):
        try:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
        except Vehicle.DoesNotExist:
            return Response(
                {"detail": "Vehicle not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Handle multiple images
        images = request.FILES.getlist('images')
        if not images:
            return Response(
                {"detail": "No images provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create image objects
        image_objects = []
        for image in images:
            vehicle_image = VehicleImage.objects.create(
                vehicle=vehicle,
                image=image,
                caption=request.data.get('caption', '')
            )
            image_objects.append(vehicle_image)

        # Serialize and return
        serializer = VehicleImageSerializer(image_objects, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VehicleDetail(generics.RetrieveAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]


class VehicleUpdate(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminUser]


class VehicleDelete(generics.DestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminUser]


# VehicleImage views
'''
class VehicleImageList(generics.ListCreateAPIView):
    serializer_class = VehicleImageSerializer
    permission_classes = [IsAuthenticatedOrReadAdmin]

    def get_queryset(self):
        queryset = VehicleImage.objects.all()
        vehicle_id = self.request.query_params.get('vehicle')
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
        return queryset
'''


class VehicleImageList(generics.ListCreateAPIView):
    serializer_class = VehicleImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return VehicleImage.objects.filter(vehicle_id=self.kwargs['vehicle_id'])

    def perform_create(self, serializer):
        vehicle = Vehicle.objects.get(pk=self.kwargs['vehicle_id'])
        serializer.save(vehicle=vehicle)


class VehicleImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageSerializer
    permission_classes = [IsAuthenticatedOrReadAdmin]


'''
# VehicleLocation views
# class VehicleLocationList(generics.ListCreateAPIView):
#     serializer_class = VehicleLocationSerializer
#     permission_classes = [IsAuthenticatedOrReadAdmin]

#     def get_queryset(self):
#         queryset = VehicleLocation.objects.all()
#         vehicle_id = self.request.query_params.get('vehicle')
#         if vehicle_id:
#             queryset = queryset.filter(vehicle_id=vehicle_id)
#         return queryset


# class VehicleLocationDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = VehicleLocation.objects.all()
#     serializer_class = VehicleLocationSerializer
#     permission_classes = [IsAuthenticatedOrReadAdmin]
'''