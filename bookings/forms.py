from django import forms

from transport.models import BusStop, Seat


class BookingForm(forms.Form):

    boarding_stop = forms.ModelChoiceField(
        queryset=BusStop.objects.none(),
        empty_label="Select boarding stop",
    )

    destination_stop = forms.ModelChoiceField(
        queryset=BusStop.objects.none(),
        empty_label="Select destination stop",
    )

    seat = forms.ModelChoiceField(
        queryset=Seat.objects.none(),
        empty_label="Select seat",
    )

    def __init__(self, *args, trip=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.trip = trip

        if trip is None:
            return

        route_stops = (
            trip.route.route_stops
            .select_related("bus_stop")
            .order_by("stop_order")
        )

        stop_ids = route_stops.values_list(
            "bus_stop_id",
            flat=True,
        )

        self.fields["boarding_stop"].queryset = (
            BusStop.objects.filter(
                id__in=stop_ids,
                is_active=True,
            )
        )

        self.fields["destination_stop"].queryset = (
            BusStop.objects.filter(
                id__in=stop_ids,
                is_active=True,
            )
        )

        self.fields["seat"].queryset = (
            Seat.objects.filter(
                vehicle=trip.vehicle,
            )
            .exclude(
                bookings__trip=trip,
                bookings__status="CONFIRMED",
            )
            .order_by("seat_number")
        )

        # Bootstrap styling

        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "form-select",
                }
            )