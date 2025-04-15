from django.contrib import admin
from .models import Dispatcher


@admin.register(Dispatcher)
class DispatcherAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'service_region')
    search_fields = ('user__email', 'employee_id')
    list_filter = ['service_region']
