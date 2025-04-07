from django.db import models
from useraccount.models import User
from vehicle.models import Vehicle


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='drivers', null=True, blank=True)
    from_state = models.CharField(max_length=50, null=True, blank=True)
    to_state = models.CharField(max_length=50, null=True, blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry_date = models.DateField()
    rating = models.FloatField(default=0.0)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    def __str__(self):
        return f"{self.user.username} - {self.vehicle.make} {self.vehicle.model}"
