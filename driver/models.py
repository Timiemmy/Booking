from django.db import models
from useraccount.models import CustomUser
from vehicle.models import Vehicle


class Driver(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='driver_profile')
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='drivers')
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry_date = models.DateField()
    rating = models.FloatField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    total_trips = models.PositiveIntegerField(default=0)
    driver_license_image = models.ImageField(
        upload_to='drivers_licenses/')
    #current_location = models.PointField(null=True, blank=True)

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    def __str__(self):
        return f"{self.user.username} - {self.vehicle.make} {self.vehicle.model}"


class DriverVerification(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    driver = models.OneToOneField(
        Driver, on_delete=models.CASCADE, related_name='verification')
    id_document = models.FileField(upload_to='driver_verification/id/')
    license_document = models.FileField(upload_to='driver_verification/license/')
    address_proof = models.FileField(
        upload_to='driver_verification/address/', null=True, blank=True)
    background_check_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    background_check_report = models.FileField(
        upload_to='verification/background/', null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return f"Verification for {self.driver.user.get_full_name()}"
