from django.db import models
from useraccount.models import User
from vehicle.models import Vehicle



class Booking(models.Model):
    TRIP_TYPES = (
        ('RT', 'Round Trip'),
        ('OW', 'One Way'),
        ('HR', 'Hourly Rental'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    trip_type = models.CharField(max_length=2, choices=TRIP_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_type = models.CharField(max_length=10, choices=[
        ('HOME', 'Home Pickup'),
        ('PARK', 'Park Meeting')
    ])
    passengers = models.PositiveIntegerField()
    luggage = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ])
