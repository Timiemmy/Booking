from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Booking


@admin.register(Booking)
class CustomAdminClass(ModelAdmin):
    pass
