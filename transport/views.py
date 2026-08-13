from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .forms import BookingForm
from .models import Trip, Booking
from .services import create_booking

# Create your views here.

@login_required
def book_trip(request, trip_id):
    trip = get_object_or_404(
        Trip.objects.select_related(
            "route",
            "vehicle",
        ),
        id=trip_id,
    )

    if request.method == "POST":
        form = BookingForm(request.POST, trip=trip)

        if form.is_valid():
            booking = form.save(commit=False)

            booking.passenger = request.user
            booking.trip = trip

            # Temporary fare.
            # We will replace this with the 5 KM fare calculation.
            booking.fare = 0

            # Temporary reference.
            # We'll improve this next.
            booking.booking_reference = (
                f"ABT-{request.user.id}-{trip.id}"
            )

            try:
                booking = create_booking(
                    passenger=request.user,
                    trip=trip,
                    boarding_stop=booking.boarding_stop,
                    destination_stop=booking.destination_stop,
                    fare=booking.fare,
                    booking_reference=booking.booking_reference,
                )

                messages.success(
                    request,
                    f"Booking successful! Reference: "
                    f"{booking.booking_reference}",
                )

                return redirect("transport:booking_success", booking_id=booking.id)

            except Exception as error:
                form.add_error(None, str(error))

    else:
        form = BookingForm(trip=trip)

    return render(
        request,
        "transport/book_trip.html",
        {
            "form": form,
            "trip": trip,
        },
    )
    
    
@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        passenger=request.user,
    )

    return render(
        request,
        "transport/booking_success.html",
        {
            "booking": booking,
        },
    )
