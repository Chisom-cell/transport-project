from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from .forms import BookingForm
from transport.models import Trip, BusStop
from .models import Booking
from .services import get_available_capacity, create_booking


@login_required
@role_required("PASSENGER")
def seat_selection(request, trip_id):
    """
    Display a trip booking page.

    We keep the function name for now so we don't
    have to change the existing URL configuration.
    There are no numbered seats.
    """
    trip = get_object_or_404(
        Trip.objects.select_related(
            "route",
            "vehicle",
        ),
        id=trip_id,
    )
    
    form = BookingForm(trip=trip)

    return render(
        request,
        "bookings/seat_selection.html",
        {
            "trip": trip,
            "form": form,
            "available_capacity": get_available_capacity(trip),
        },
    )

@login_required
@role_required("PASSENGER")
def confirm_booking(request, trip_id):

    trip = get_object_or_404(
        Trip.objects.select_related(
            "route",
            "vehicle",
        ),
        id=trip_id,
    )

    if request.method != "POST":
        return redirect(
            "bookings:seat_selection",
            trip_id=trip.id,
        )

    form = BookingForm(
        request.POST,
        trip=trip,
    )

    if form.is_valid():

        try:
            booking = create_booking(
                passenger=request.user,
                trip=trip,
                boarding_stop=form.cleaned_data[
                    "boarding_stop"
                ],
                destination_stop=form.cleaned_data[
                    "destination_stop"
                ],
                seat=form.cleaned_data["seat"],
            )

            return redirect(
                "bookings:booking_detail",
                booking_id=booking.id,
            )

        except ValidationError as e:

            form.add_error(
                None,
                str(e),
            )

    return render(
        request,
        "bookings/seat_selection.html",
        {
            "trip": trip,
            "form": form,
            "available_capacity": get_available_capacity(trip),
        },
    )


@login_required
@role_required("PASSENGER")
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
@role_required("PASSENGER")
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
@role_required("PASSENGER")
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

    return redirect("bookings:my_bookings")


