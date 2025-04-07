from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Vehicle, VehicleImage, VehicleType, Amenity



@admin.register(Vehicle)
class VehicleAdminClass(ModelAdmin):
    pass


@admin.register(VehicleImage)
class VehicleImageAdminClass(ModelAdmin):
    pass


@admin.register(VehicleType)
class VehicleTypeAdminClass(ModelAdmin):
    pass


@admin.register(Amenity)
class AmenityAdminClass(ModelAdmin):
    pass