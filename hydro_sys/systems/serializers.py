from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from .models import HydroponicSystem, Measurement


class MeasurementPagination(PageNumberPagination):
    page_size = 10


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


class HydroponicSystemDetailSerializer(serializers.ModelSerializer):
    measurements = serializers.SerializerMethodField()

    class Meta:
        model = HydroponicSystem
        fields = ("id", "name", "type", "timestamp", "description", "measurements")

    def get_measurements(self, obj):
        request = self.context.get("request")
        measurements = obj.measurements.all()

        paginator = MeasurementPagination()
        paginated_measurements = paginator.paginate_queryset(measurements, request)

        return paginator.get_paginated_response(
            MeasurementSerializer(paginated_measurements, many=True).data
        ).data
