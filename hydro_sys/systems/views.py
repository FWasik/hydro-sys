from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import HydroponicSystem, Measurement
from .serializers import (
    HydroponicSystemDetailSerializer,
    HydroponicSystemListSerializer,
    MeasurementSerializer,
)
from .filters import MeasurementFilter, HydroponicSystemFilter


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering = ["-timestamp"]


class HydroponicSystemViewSet(BaseModelViewSet):
    filterset_class = HydroponicSystemFilter
    ordering_fields = ["timestamp", "name", "type"]

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return HydroponicSystemDetailSerializer

        return HydroponicSystemListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MeasurementViewSet(BaseModelViewSet):
    serializer_class = MeasurementSerializer
    filterset_class = MeasurementFilter
    ordering_fields = ["ph", "tds", "temperature", "timestamp", "system"]

    def get_queryset(self):
        return Measurement.objects.filter(system__owner=self.request.user)

    def perform_create(self, serializer):
        system = serializer.validated_data["system"]

        if system.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to add measurements to this system."
            )

        serializer.save()
