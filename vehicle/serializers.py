from rest_framework import serializers
from .models import VehicleType, Vehicle, Amenity, VehicleImage


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'icon', 'number']


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ['id', 'name', 'description']


class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ['id', 'image', 'caption']


class VehicleImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ['image', 'caption']


'''
class VehicleLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleLocation
        fields = ['id', 'latitude', 'longitude',
                  'speed', 'heading', 'timestamp']
'''


class VehicleSerializer(serializers.ModelSerializer):
    category = VehicleTypeSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True)
    driver_name = serializers.SerializerMethodField()
    driver_email = serializers.SerializerMethodField()
    # locations = VehicleLocationSerializer(many=True, read_only=True)

    # For write operations
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=VehicleType.objects.all(),
        write_only=True,
        source='category',
        many=True,
        required=False
    )
    amenity_ids = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(),
        write_only=True,
        source='amenities',
        many=True,
        required=False
    )

    class Meta:
        model = Vehicle
        fields = '__all__'
        extra_kwargs = {
            # Hide VIN in read operations for security
            'vin': {'write_only': True}
        }

    def get_driver_name(self, obj):
            # Use the related_name 'drivers' to get the driver
        driver = getattr(obj, 'drivers', None)
        if driver:
            return driver.user.get_full_name()
        return None

    def get_driver_email(self, obj):
        driver = getattr(obj, 'drivers', None)
        if driver:
            return driver.user.email
        return None


class VehicleCreateSerializer(VehicleSerializer):
    images = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    image_captions = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta(VehicleSerializer.Meta):
        fields = ['id', 'name', 'description', 'category', 'amenities', 'images', 'image_captions', 'category_ids', 'amenity_ids', 'vin', 'make', 'model', 'year', 'color',
                  'license_plate', 'status', 'daily_rate', 'weekly_rate', 'monthly_rate', 'mileage', 'fuel_type', 'transmission', 'seats', 'doors', 'luggage_capacity', 'features', 'notes']
