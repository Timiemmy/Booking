from rest_framework import serializers
from .models import ComapanyLocation


class CompanyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComapanyLocation
        fields = '__all__'