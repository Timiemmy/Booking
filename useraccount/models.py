from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.conf import settings


class CustomUser(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(unique=True)  # Make email the unique identifier
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_image = models.ImageField(
        upload_to='User_profile_image/', null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_driver = models.BooleanField(default=False)
    is_two_factor_enabled = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Set email as the authentication field
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Remove email from required fields


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['date_joined']

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f" {self.user} - {self.street}, {self.city}, {self.state}, {self.zip_code}, {self.country}"

