from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Booking


@transaction.atomic
def create_booking(
    passenger,
    trip,
    boarding_stop,
    destination_stop,
    fare,
    booking_reference,
):
    if trip.available_capacity <= 0:
        raise ValidationError("This trip is full.")

    if trip.status in ["CANCELLED", "ARRIVED"]:
        raise ValidationError(
            "This trip is no longer available for booking."
        )

    route_stops = trip.route.route_stops.all()

    valid_stop_ids = route_stops.values_list(
        "bus_stop_id",
        flat=True,
    )

    if boarding_stop.id not in valid_stop_ids:
        raise ValidationError(
            "The boarding stop is not part of this route."
        )

    if destination_stop.id not in valid_stop_ids:
        raise ValidationError(
            "The destination stop is not part of this route."
        )

    if boarding_stop.id == destination_stop.id:
        raise ValidationError(
            "Boarding and destination stops cannot be the same."
        )

    booking = Booking.objects.create(
        passenger=passenger,
        trip=trip,
        boarding_stop=boarding_stop,
        destination_stop=destination_stop,
        fare=fare,
        booking_reference=booking_reference,
    )

    return booking