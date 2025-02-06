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


class HydroponicSystemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroponicSystem
        fields = ("id", "name", "type", "timestamp", "description")


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
