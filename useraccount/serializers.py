from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import CustomUser, Address


class AddressSerializer(ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Address
        fields = ['id', 'user', 'user_name', 'street', 'city', 'state', 'zip_code', 'country']
        read_only_fields = ['id', 'user']

class UserSerializer(ModelSerializer):
    address = SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'is_driver', 
                  'date_joined', 'is_active', 'address']
        read_only_fields = ['id', 'date_joined']


    def get_address(self, obj):
        try:
            address = Address.objects.get(user=obj)
            return AddressSerializer(address, context=self.context).data
        except Address.DoesNotExist:
            return None

