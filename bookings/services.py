from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Booking


def get_available_capacity(trip):
    """
    Return the number of passenger spaces still available
    on a trip.
    """

    capacity = trip.vehicle.capacity

    confirmed_bookings = Booking.objects.filter(
        trip=trip,
        status=Booking.Status.CONFIRMED,
    ).count()

    return max(capacity - confirmed_bookings, 0)


@transaction.atomic
def create_booking(
    passenger,
    trip,
    boarding_stop,
    destination_stop,
):
    """
    Create a booking if the vehicle still has available capacity.
    """

    # Lock the trip while checking capacity so two bookings
    # cannot consume the same final space at the same time.
    trip = type(trip).objects.select_for_update().get(pk=trip.pk)

    available_capacity = get_available_capacity(trip)

    if available_capacity <= 0:
        raise ValidationError(
            "This trip is full. Please choose another trip."
        )

    booking = Booking.objects.create(
        passenger=passenger,
        trip=trip,
        boarding_stop=boarding_stop,
        destination_stop=destination_stop,
        status=Booking.Status.CONFIRMED,
    )

    return booking