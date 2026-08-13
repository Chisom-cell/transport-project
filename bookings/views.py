from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from transport.models import Trip, BusStop
from .models import Booking
from .services import get_available_capacity, create_booking


@login_required
def seat_selection(request, trip_id):
    """
    Display a trip booking page.

    We keep the function name for now so we don't
    have to change the existing URL configuration.
    There are no numbered seats.
    """

    trip = get_object_or_404(Trip, id=trip_id)

    available_capacity = get_available_capacity(trip)

    # Get the stops belonging to this trip's route
    route_stops = trip.route.route_stops.select_related(
        "bus_stop"
    ).order_by("stop_order")

    return render(
        request,
        "bookings/seat_selection.html",
        {
            "trip": trip,
            "available_capacity": available_capacity,
            "route_stops": route_stops,
        },
    )


@login_required
def confirm_booking(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    if request.method == "POST":

        boarding_stop = get_object_or_404(
            BusStop,
            id=request.POST.get("boarding_stop_id"),
        )

        destination_stop = get_object_or_404(
            BusStop,
            id=request.POST.get("destination_stop_id"),
        )

        try:
            booking = create_booking(
                passenger=request.user,
                trip=trip,
                boarding_stop=boarding_stop,
                destination_stop=destination_stop,
            )

            return redirect(
                "booking_detail",
                booking.id,
            )

        except ValidationError as e:
            route_stops = trip.route.route_stops.select_related(
                "bus_stop"
            ).order_by("stop_order")

            return render(
                request,
                "bookings/seat_selection.html",
                {
                    "trip": trip,
                    "available_capacity": get_available_capacity(trip),
                    "route_stops": route_stops,
                    "error": str(e),
                },
            )

    return redirect("seat_selection", trip_id=trip.id)


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        passenger=request.user
    ).order_by("-created_at")

    return render(
        request,
        "bookings/my_bookings.html",
        {
            "bookings": bookings,
        },
    )


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        passenger=request.user,
    )

    return render(
        request,
        "bookings/booking_detail.html",
        {
            "booking": booking,
        },
    )


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        passenger=request.user,
    )

    if (
        booking.trip.status in ("SCHEDULED", "BOARDING")
        and booking.status == Booking.Status.CONFIRMED
    ):
        booking.status = Booking.Status.CANCELLED
        booking.save()

    return redirect("my_bookings")