from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from allauth.account.adapter import get_adapter
from .models import CustomUser, Address

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    username = None  # Remove username field
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        password = self.validated_data.get('password', '')
        return {
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': password,
            'password2': password,
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save()
        return user


class AddressSerializer(ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'user', 'user_name', 'street',
                  'city', 'state', 'zip_code', 'country']
        read_only_fields = ['id', 'user']


class CustomUserSerializer(ModelSerializer):
    address = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'is_driver',
                  'date_joined', 'is_active', 'is_two_factor_enabled', 'phone_verified', 'is_staff', 'address']
        read_only_fields = ['id', 'date_joined']

    def get_address(self, obj):
        try:
            address = Address.objects.get(user=obj)
            return AddressSerializer(address, context=self.context).data
        except Address.DoesNotExist:
            return None
