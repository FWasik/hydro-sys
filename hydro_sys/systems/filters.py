import django_filters
from .models import Measurement, HydroponicSystem


class BaseFilter(django_filters.FilterSet):
    datetime_from = django_filters.IsoDateTimeFilter(
        field_name="timestamp", lookup_expr="gte", label="From Datetime"
    )
    datetime_to = django_filters.IsoDateTimeFilter(
        field_name="timestamp", lookup_expr="lte", label="To Datetime"
    )

    class Meta:
        abstract = True


class MeasurementFilter(BaseFilter):
    ph_min = django_filters.NumberFilter(
        field_name="ph", lookup_expr="gte", label="Min pH"
    )
    ph_max = django_filters.NumberFilter(
        field_name="ph", lookup_expr="lte", label="Max pH"
    )
    tds_min = django_filters.NumberFilter(
        field_name="tds", lookup_expr="gte", label="Min TDS"
    )
    tds_max = django_filters.NumberFilter(
        field_name="tds", lookup_expr="lte", label="Max TDS"
    )
    temperature_min = django_filters.NumberFilter(
        field_name="temperature", lookup_expr="gte", label="Min Temperature"
    )
    temperature_max = django_filters.NumberFilter(
        field_name="temperature", lookup_expr="lte", label="Max Temperature"
    )

    class Meta:
        model = Measurement
        fields = ("ph", "tds", "temperature", "timestamp")


class HydroponicSystemFilter(BaseFilter):
    type = django_filters.ChoiceFilter(choices=HydroponicSystem.types)

    class Meta:
        model = HydroponicSystem
        fields = ("timestamp",)
