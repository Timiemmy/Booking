# dispatchers/models.py
from django.db import models
from useraccount.models import CustomUser
from companylocation.models import ComapanyLocation


class Dispatcher(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='dispatcher_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    service_region = models.OneToOneField(
        ComapanyLocation, on_delete=models.SET_NULL, null=True, blank=True, related_name='dispatcher_location')

    def __str__(self):
        return f"Dispatcher: {self.user.email}"
