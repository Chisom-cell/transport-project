from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import (
    Organization,
    BusStop,
    Route,
    RouteStop,
    Vehicle,
    DriverProfile,
    Trip,   
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "organization_type", "is_active", "created_at")
    list_filter = ("organization_type", "is_active")
    search_fields = ("name",)


@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "origin",
        "destination",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "origin", "destination")


@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = (
        "route",
        "bus_stop",
        "stop_order",
        "distance_from_origin_km",
    )
    list_filter = ("route",)
    search_fields = ("route__name", "bus_stop__name")
    ordering = ("route", "stop_order")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle_code",
        "registration_number",
        "organization",
        "vehicle_type",
        "capacity",
        "status",
    )
    list_filter = ("organization", "vehicle_type", "status")
    search_fields = (
        "vehicle_code",
        "registration_number",
        "organization__name",
    )


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "organization",
        "license_number",
        "is_active",
    )
    list_filter = ("organization", "is_active")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "license_number",
    )


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
        "route",
        "vehicle",
        "driver",
        "departure_time",
        "status",
        "current_stop",
        "total_capacity",
        "booked_capacity",
        "available_capacity",
    )
    
    list_filter = ("organization", "status", "route")
    
    search_fields = (
        "route__name",
        "vehicle__vehicle_code",
        "driver__user__username",
    )
    ordering = ("-departure_time",)


