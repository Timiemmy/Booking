from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Driver


@admin.register(Driver)
class DriverAdminClass(ModelAdmin):
    list_display = ('user', 'vehicle', 'license_number', 'rating')
