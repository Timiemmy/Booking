from django.urls import path
from .views import (
    VehicleTypeList, VehicleTypeDetail,
    VehicleList, VehicleDetail, VehicleUpdate, VehicleDelete,
    AmenityList, AmenityDetail,
    VehicleImageList, VehicleImageDetail, VehicleCreateWithImages, VehicleUpdateWithImages, VehicleImageUpload
)

app_name = 'vehicle'


urlpatterns = [
    # Vehicle Type URLs
    path('category/', VehicleTypeList.as_view(), name='vehicletype-list'),
    path('category/<int:pk>/', VehicleTypeDetail.as_view(),
         name='vehicletype-detail'),

    # Vehicle URLs
    path('', VehicleList.as_view(), name='vehicle-list'),
    path('<int:pk>/', VehicleDetail.as_view(), name='vehicle-detail'),
    path('<int:pk>/update/',
         VehicleUpdate.as_view(), name='vehicle-update'),
    path('<int:pk>/delete/',
         VehicleDelete.as_view(), name='vehicle-delete'),

    # Combined endpoint for vehicle and images
    path('create', VehicleCreateWithImages.as_view(),
         name='vehicle-create-with-images'),
    path('<int:pk>/update/',
         VehicleUpdateWithImages.as_view(), name='vehicle-update-with-images'),

    # Amenity URLs
    path('amenities/', AmenityList.as_view(), name='amenity-list'),
    path('amenities/<int:pk>/', AmenityDetail.as_view(), name='amenity-detail'),

    # Vehicle Image URLs
    path('images/', VehicleImageList.as_view(), name='vehicleimage-list'),
    path('images/<int:pk>/', VehicleImageDetail.as_view(),
         name='vehicleimage-detail'),

    #for existing vehicles which can be deleted later.
    path('vehicles/<int:vehicle_id>/upload-images/',
         VehicleImageUpload.as_view(), name='vehicle-image-upload'),

    # Vehicle Location URLs
    # path('vehicle-locations/', VehicleLocationList.as_view(),
    #      name='vehiclelocation-list'),
    # path('vehicle-locations/<int:pk>/', VehicleLocationDetail.as_view(),
    #      name='vehiclelocation-detail'),
]
