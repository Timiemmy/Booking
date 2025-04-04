from rest_framework.serializers import ModelSerializer
from .models import User, Address


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'is_driver', 'date_joined', 'is_active']
        read_only_fields = ['id', 'date_joined']


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'street', 'city', 'state', 'zip_code', 'country']
        read_only_fields = ['id', 'user']