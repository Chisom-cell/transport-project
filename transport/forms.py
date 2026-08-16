from django import forms

from .models import (
    Organization,
    BusStop,
    Route,
    RouteStop,
    Vehicle,
    DriverProfile,
    Trip,
    FareBand,
)


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            "name",
            "organization_type",
            "is_active",
        ]


class BusStopForm(forms.ModelForm):
    class Meta:
        model = BusStop
        fields = [
            "name",
            "description",
            "latitude",
            "longitude",
            "is_active",
        ]


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = [
            "name",
            "origin",
            "destination",
            "is_active",
        ]


class RouteStopForm(forms.ModelForm):
    class Meta:
        model = RouteStop
        fields = [
            "route",
            "bus_stop",
            "stop_order",
            "distance_from_origin_km",
        ]


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "organization",
            "vehicle_code",
            "registration_number",
            "vehicle_type",
            "capacity",
            "status",
            "maintenance_note",
        ]


class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = [
            "user",
            "organization",
            "license_number",
            "is_active",
        ]


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            "organization",
            "route",
            "vehicle",
            "driver",
            "departure_time",
            "status",
            "current_stop",
        ]

        widgets = {
            "departure_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
        }


class FareBandForm(forms.ModelForm):
    class Meta:
        model = FareBand
        fields = [
            "min_distance_km",
            "max_distance_km",
            "amount",
            "is_active",
        ]