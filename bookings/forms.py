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

        # ---------------------------------------------------------
        # Get stops belonging to this trip's route
        # ---------------------------------------------------------

        self.route_stops = list(
            trip.route.route_stops
            .select_related("bus_stop")
            .order_by("stop_order")
        )

        stop_ids = [
            route_stop.bus_stop_id
            for route_stop in self.route_stops
        ]

        # ---------------------------------------------------------
        # Boarding stops
        # ---------------------------------------------------------

        self.fields["boarding_stop"].queryset = (
            BusStop.objects.filter(
                id__in=stop_ids,
                is_active=True,
            )
        )

        # ---------------------------------------------------------
        # Destination stops
        # ---------------------------------------------------------

        self.fields["destination_stop"].queryset = (
            BusStop.objects.filter(
                id__in=stop_ids,
                is_active=True,
            )
        )

        # ---------------------------------------------------------
        # Available seats for this trip
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # Bootstrap styling
        # ---------------------------------------------------------

        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "form-select",
                }
            )

    def clean(self):
        cleaned_data = super().clean()

        boarding_stop = cleaned_data.get("boarding_stop")
        destination_stop = cleaned_data.get("destination_stop")

        # ---------------------------------------------------------
        # Make sure both stops were selected
        # ---------------------------------------------------------

        if not boarding_stop or not destination_stop:
            return cleaned_data

        # ---------------------------------------------------------
        # Boarding and destination cannot be the same
        # ---------------------------------------------------------

        if boarding_stop.id == destination_stop.id:
            raise forms.ValidationError(
                "Boarding and destination stops cannot be the same."
            )

        # ---------------------------------------------------------
        # Find the position of each stop on the route
        # ---------------------------------------------------------

        boarding_order = None
        destination_order = None

        for route_stop in self.route_stops:

            if route_stop.bus_stop_id == boarding_stop.id:
                boarding_order = route_stop.stop_order

            if route_stop.bus_stop_id == destination_stop.id:
                destination_order = route_stop.stop_order

        # ---------------------------------------------------------
        # Make sure boarding stop belongs to route
        # ---------------------------------------------------------

        if boarding_order is None:
            self.add_error(
                "boarding_stop",
                "The selected boarding stop is not part of this route.",
            )

        # ---------------------------------------------------------
        # Make sure destination stop belongs to route
        # ---------------------------------------------------------

        if destination_order is None:
            self.add_error(
                "destination_stop",
                "The selected destination stop is not part of this route.",
            )

        if boarding_order is None or destination_order is None:
            return cleaned_data

        # ---------------------------------------------------------
        # Destination must come after boarding stop
        # ---------------------------------------------------------

        if destination_order <= boarding_order:
            self.add_error(
                "destination_stop",
                "The destination stop must come after the boarding stop.",
            )

        return cleaned_data