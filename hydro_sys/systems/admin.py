from django.contrib import admin
from .models import HydroponicSystem, Measurement


@admin.register(HydroponicSystem)
class HydroponicSystemAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "owner", "timestamp")
    list_filter = ("type", "owner")
    search_fields = ("name", "owner__username")
    ordering = ("-timestamp",)
    date_hierarchy = "timestamp"

    fieldsets = (
        ("Basic Info", {"fields": ("name", "type", "description")}),
        ("Ownership", {"fields": ("owner",)}),
        ("Timestamps", {"fields": ("timestamp",)}),
    )

    readonly_fields = ("timestamp",)


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ("system", "ph", "temperature", "tds", "timestamp", "description")
    search_fields = ("system__name", "ph", "temperature", "tds", "description")
    list_filter = ("system", "timestamp", "ph", "temperature", "tds")
    list_editable = ("ph", "temperature", "tds")
    ordering = ("-timestamp",)
    date_hierarchy = "timestamp"

    fieldsets = (
        (
            "Measurement Info",
            {"fields": ("system", "ph", "temperature", "tds", "description")},
        ),
        ("Timestamps", {"fields": ("timestamp",)}),
    )

    readonly_fields = ("timestamp",)
