# agents/models.py
from django.db import models
from useraccount.models import CustomUser
from companylocation.models import ComapanyLocation


class Agent(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='agent_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    service_region = models.OneToOneField(
        ComapanyLocation, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_location')


    def __str__(self):
        return f"Agent: {self.user.email}"

    def save(self, *args, **kwargs):
        # Add user to Agent group
        from django.contrib.auth.models import Group
        agent_group, created = Group.objects.get_or_create(name='Agent')
        self.user.groups.add(agent_group)

        super().save(*args, **kwargs)
