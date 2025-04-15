from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin, StackedInline
from unfold.forms import AdminPasswordChangeForm, UserCreationForm, UserChangeForm
from .models import CustomUser, Address


admin.site.unregister(Group)


class AddressInline(StackedInline):
    model = Address
    can_delete = False
    verbose_name_plural = 'Address'
    ordering = ('-id',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'country')
    search_fields = ('user__email', 'city', 'state', 'country')


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    model = CustomUser
    list_display = ('email', 'first_name', 'last_name',
                    'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # Specify which fields should be editable
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',
         'email', 'phone', 'emergency_contact', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_driver',
         'is_two_factor_enabled', 'phone_verified', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    inlines = [AddressInline]


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
