from transport.models import Seat
from .models import Booking
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError

from transport.models import Seat
from .models import Booking, FareBand


def get_available_seats(trip):
    booked_seat_ids = Booking.objects.filter(
        trip=trip,
        status=Booking.Status.CONFIRMED,
    ).values_list("seat_id", flat=True)

    return Seat.objects.filter(
        vehicle=trip.vehicle
    ).exclude(id__in=booked_seat_ids).order_by("seat_number")
    
    
def calculate_fare(boarding_stop, destination_stop):

 def get_available_seats(trip):
    booked_seat_ids = Booking.objects.filter(
        trip=trip,
        status=Booking.Status.CONFIRMED,
    ).values_list("seat_id", flat=True)

    return Seat.objects.filter(
        vehicle=trip.vehicle
    ).exclude(id__in=booked_seat_ids).order_by("seat_number")


@transaction.atomic
def create_booking(passenger, trip, seat, boarding_stop, destination_stop):
    existing = Booking.objects.select_for_update().filter(
        trip=trip,
        seat=seat,
        status=Booking.Status.CONFIRMED,
    )
    if existing.exists():
        raise ValidationError("This seat has just been booked. Please choose another.")

    distance, fare = calculate_fare(boarding_stop, destination_stop)

    return Booking.objects.create(
        passenger=passenger,
        trip=trip,
        seat=seat,
        boarding_stop=boarding_stop,
        destination_stop=destination_stop,
        fare=fare,
    )