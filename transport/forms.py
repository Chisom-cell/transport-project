from django import forms

from .models import Booking, BusStop


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "boarding_stop",
            "destination_stop",
        ]

        widgets = {
            "boarding_stop": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "destination_stop": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, trip=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.trip = trip

        if trip:
            route_stops = trip.route.route_stops.select_related(
                "bus_stop"
            )

            stops = [
                (route_stop.bus_stop.id, route_stop.bus_stop.name)
                for route_stop in route_stops
            ]

            self.fields["boarding_stop"].choices = [
                ("", "Select boarding stop")
            ] + stops

            self.fields["destination_stop"].choices = [
                ("", "Select destination stop")
            ] + stops