# admin_users/models.py
from django.db import models
from useraccount.models import CustomUser
from companylocation.models import ComapanyLocation


class AdminUser(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    service_region = models.ForeignKey(
        ComapanyLocation, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_location')

    def __str__(self):
        return f"Admin: {self.user.email}"

