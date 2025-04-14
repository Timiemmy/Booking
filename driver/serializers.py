from rest_framework import serializers
from vehicle.serializers import VehicleSerializer
from .models import Driver, DriverVerification


class DriverSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source='vehicle.make', read_only=True)
    vehicle_model = serializers.CharField(source='vehicle.model', read_only=True)
    driver_email = serializers.CharField(source='user.email', read_only=True)
    driver_name = serializers.SerializerMethodField()
    class Meta:
        model = Driver
        fields = [
            'id', 'driver_email', 'driver_name', 'vehicle', 'vehicle_name', 'vehicle_model', 'license_number',
            'license_expiry_date', 'rating', 'is_available', 'total_trips',
            'driver_license_image'
        ]

    def get_driver_name(self, obj):
        return obj.user.get_full_name() if obj.user else None



class DriverVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverVerification
        fields = [
            'id', 'driver', 'driver_name', 'id_document',
            'license_document', 'address_proof', 'background_check_status',
            'background_check_report', 'verification_notes', 'verified_at',
            'verified_by', 'verified_by_id', 'rejection_reason'
        ]
