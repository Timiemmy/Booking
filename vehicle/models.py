from django.db import models


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
    capacity = models.PositiveIntegerField(default=1, blank=True)
    is_active = models.BooleanField(default=True)
    from_state = models.CharField(max_length=50, null=True, blank=True)
    to_state = models.CharField(max_length=50, null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    estimated_arrival_time = models.DateTimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    has_entourage_option = models.BooleanField(default=False)
    has_security_option = models.BooleanField(default=False)
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)

    fuel_type = models.CharField(max_length=20, blank=True)
    fuel_efficiency = models.FloatField(null=True, blank=True)  # km/L
    has_gps_tracker = models.BooleanField(default=False)
    tracker_id = models.CharField(max_length=50, blank=True)

    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    daily_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def __str__(self):
        make = self.make or "Unknown Make"
        model = self.model or "Unknown Model"
        year = self.year or "Unknown Year"
        return f"{make} {model} ({year})"


class Amenity(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=30, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicle_images/')
    caption = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.vehicle}"


class VehicleLocation(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name='locations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed = models.FloatField(null=True, blank=True)  # km/h
    heading = models.FloatField(null=True, blank=True)  # degrees
    timestamp = models.DateTimeField(auto_now_add=True)

    # If using GeoDjango
    # position = models.PointField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['vehicle', 'timestamp']),
        ]

    # def save(self, *args, **kwargs):
    #     if not self.position and self.latitude and self.longitude:
    #         self.position = Point(float(self.longitude), float(self.latitude))
    #     super().save(*args, **kwargs)
