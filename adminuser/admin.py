from django.contrib import admin
from .models import AdminUser


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_region')
    search_fields = ('user__email', 'department')
