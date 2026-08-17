import uuid

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Booking
from transport.models import FareBand, Seat, Trip


def get_available_capacity(trip):
    """
    Return the number of passenger spaces still available
    on a trip.
    """

    confirmed_bookings = Booking.objects.filter(
        trip=trip,
        status=Booking.Status.CONFIRMED,
    ).count()

    return max(
        trip.vehicle.capacity - confirmed_bookings,
        0,
    )


def calculate_trip_distance(
    trip,
    boarding_stop,
    destination_stop,
):
    """
    Calculate the distance between two stops on the trip's route.

    Travel is allowed in either direction.

    Example:
        Umuahia → Aba
        Aba → Umuahia

    Both journeys use the absolute distance between
    the two stops.
    """

    route_stops = (
        trip.route.route_stops
        .select_related("bus_stop")
        .all()
    )

    boarding_route_stop = None
    destination_route_stop = None

    for route_stop in route_stops:

        if route_stop.bus_stop_id == boarding_stop.id:
            boarding_route_stop = route_stop

        if route_stop.bus_stop_id == destination_stop.id:
            destination_route_stop = route_stop

    if boarding_route_stop is None:
        raise ValidationError(
            "The boarding stop is not part of this route."
        )

    if destination_route_stop is None:
        raise ValidationError(
            "The destination stop is not part of this route."
        )

    if (
        boarding_route_stop.bus_stop_id
        == destination_route_stop.bus_stop_id
    ):
        raise ValidationError(
            "Boarding and destination stops cannot be the same."
        )

    distance = abs(
        destination_route_stop.distance_from_origin_km
        - boarding_route_stop.distance_from_origin_km
    )

    if distance <= 0:
        raise ValidationError(
            "The journey distance must be greater than zero."
        )

    return distance


def calculate_fare(
    trip,
    boarding_stop,
    destination_stop,
):
    """
    Find the active fare configured for this journey.

    The fare is determined by:

        Route
        + Boarding Stop
        + Destination Stop

    Example:

        Umuahia → Aba
        Umuahia Terminal → Isialangwa
        = ₦1,200
    """

    from transport.models import RouteFare

    fare = (
        RouteFare.objects
        .filter(
            route=trip.route,
            boarding_stop=boarding_stop,
            destination_stop=destination_stop,
            is_active=True,
        )
        .first()
    )

    if fare is None:
        raise ValidationError(
            "No fare has been configured for this journey. "
            "Please choose another boarding and destination stop."
        )

    return fare.amount


def generate_booking_reference():
    """
    Generate a unique booking reference.

    Example:
        ABT-8F42C91A3B7D
    """

    while True:
        reference = f"ABT-{uuid.uuid4().hex[:12].upper()}"

        if not Booking.objects.filter(
            booking_reference=reference
        ).exists():
            return reference


@transaction.atomic
def create_booking(
    passenger,
    trip,
    boarding_stop,
    destination_stop,
    seat,
):
    """
    Create and confirm a booking safely.

    This function is the single source of truth for booking creation.
    """

    # ---------------------------------------------------------
    # 1. Lock the trip
    # ---------------------------------------------------------

    trip = (
        Trip.objects
        .select_for_update()
        .select_related(
            "vehicle",
            "route",
        )
        .get(pk=trip.pk)
    )

    # ---------------------------------------------------------
    # 2. Check trip status
    # ---------------------------------------------------------

    if trip.status not in (
        Trip.Status.SCHEDULED,
        Trip.Status.BOARDING,
    ):
        raise ValidationError(
            "This trip is no longer available for booking."
        )

    # ---------------------------------------------------------
    # 3. Validate selected seat
    # ---------------------------------------------------------

    try:
        seat = (
            Seat.objects
            .select_for_update()
            .get(pk=seat.pk)
        )
    except Seat.DoesNotExist:
        raise ValidationError(
            "The selected seat does not exist."
        )

    if seat.vehicle_id != trip.vehicle_id:
        raise ValidationError(
            "The selected seat does not belong to this vehicle."
        )

    # ---------------------------------------------------------
    # 4. Prevent double booking
    # ---------------------------------------------------------

    seat_already_booked = Booking.objects.filter(
        trip=trip,
        seat=seat,
        status=Booking.Status.CONFIRMED,
    ).exists()

    if seat_already_booked:
        raise ValidationError(
            "This seat has already been booked. "
            "Please select another seat."
        )

    # ---------------------------------------------------------
    # 5. Check vehicle capacity
    # ---------------------------------------------------------

    available_capacity = get_available_capacity(trip)

    if available_capacity <= 0:
        raise ValidationError(
            "This trip is full. Please choose another trip."
        )

    # ---------------------------------------------------------
    # 6. Validate boarding and destination stops
    # ---------------------------------------------------------

    distance = calculate_trip_distance(
        trip=trip,
        boarding_stop=boarding_stop,
        destination_stop=destination_stop,
    )

    # ---------------------------------------------------------
    # 7. Calculate fare
    # ---------------------------------------------------------

    fare = calculate_fare(
        trip=trip,
        boarding_stop=boarding_stop,
        destination_stop=destination_stop,
    )

    # ---------------------------------------------------------
    # 8. Generate booking reference
    # ---------------------------------------------------------

    booking_reference = generate_booking_reference()

    # ---------------------------------------------------------
    # 9. Create booking
    # ---------------------------------------------------------

    booking = Booking.objects.create(
        passenger=passenger,
        trip=trip,
        seat=seat,
        boarding_stop=boarding_stop,
        destination_stop=destination_stop,
        fare=fare,
        booking_reference=booking_reference,
        status=Booking.Status.CONFIRMED,
    )

    return booking