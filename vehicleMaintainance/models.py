from django.db import models
from vehicle.models import Vehicle
# Create your models here.


class MaintenanceRecord(models.Model):
    MAINTENANCE_TYPE = (
        ('routine', 'Routine Checkup'),
        ('repair', 'Repair'),
        ('inspection', 'Inspection'),
        ('oil_change', 'Oil Change'),
        ('tire_change', 'Tire Change'),
    )

    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(
        max_length=20, choices=MAINTENANCE_TYPE)
    description = models.TextField()
    date_performed = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    mileage_at_service = models.PositiveIntegerField()
    performed_by = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_mileage = models.PositiveIntegerField(
        null=True, blank=True)

    def __str__(self):
        return f"{self.maintenance_type} for {self.vehicle.license_plate} on {self.date_performed}"
