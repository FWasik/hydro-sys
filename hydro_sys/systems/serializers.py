from rest_framework import serializers
from .models import HydroponicSystem, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    system = serializers.SlugRelatedField(
        queryset=HydroponicSystem.objects.all(), slug_field="name"
    )

    class Meta:
        model = Measurement
        fields = "__all__"

    def validate_ph(self, value):
        if not (0 <= value <= 14):
            raise serializers.ValidationError("pH value must be between 0 and 14")

        return value

    def validate_tds(self, value):
        if value < 0:
            raise serializers.ValidationError("TDS must be equal to or greater than 0")

        return value


class HydroponicSystemSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = HydroponicSystem
        fields = ("id", "name", "type", "created_at", "description", "measurements")
