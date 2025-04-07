from django.db import models
from useraccount.models import User


class VehicleType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Vehicle Type'
        verbose_name_plural = 'Vehicle Types'
        ordering = ['name']

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    category = models.ManyToManyField(VehicleType)
    color = models.CharField(max_length=30, null=True, blank=True)
    license_plate = models.CharField(max_length=15, unique=True)
    vin = models.CharField(max_length=17, unique=True)
    amenities = models.ManyToManyField('Amenity')
    total_seats = models.PositiveIntegerField(default=1, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    from_state = models.CharField(max_length=50, null=True, blank=True)
    to_state = models.CharField(max_length=50, null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    estimated_arrival_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class Amenity(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=30, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicle_images/')
    caption = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.vehicle}"
