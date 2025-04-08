from django.db import models
from useraccount.models import CustomUser
from vehicle.models import Vehicle



class Booking(models.Model):
    TRIP_TYPES = (
        ('RT', 'Round Trip'),
        ('OW', 'One Way'),
        ('HR', 'Hourly Rental'),
        ('DR', 'Daily Rental')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    trip_type = models.CharField(max_length=2, choices=TRIP_TYPES)
    pickup_type = models.CharField(max_length=10, choices=[
        ('HOME', 'Home Pickup'),
        ('PARK', 'Park Meeting')
    ])
    pickup_address = models.TextField(blank=True, null=True)
    people = models.PositiveIntegerField() # how many people booking for
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateTimeField()
    luggage = models.PositiveIntegerField()
    with_entourage = models.BooleanField(default=False)
    with_security = models.BooleanField(default=False)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ])

    actual_pickup_time = models.DateTimeField(null=True, blank=True)
    actual_dropoff_time = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    cancellation_reason = models.TextField(blank=True)
    cancellation_time = models.DateTimeField(null=True, blank=True)

    #for more security
    booking_code = models.CharField(max_length=10, unique=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    is_checked_in = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
