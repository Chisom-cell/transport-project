from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from transport.models import Trip, Seat, BusStop
from .models import Booking
from .services import get_available_seats, create_booking

@login_required
def seat_selection(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    available_seats = get_available_seats(trip)
    return render(request, "bookings/seat_selection.html", {
        "trip": trip,
        "seats": available_seats,
    })

@login_required
def confirm_booking(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == "POST":
        seat = get_object_or_404(Seat, id=request.POST["seat_id"])
        boarding_stop = get_object_or_404(BusStop, id=request.POST["boarding_stop_id"])
        destination_stop = get_object_or_404(BusStop, id=request.POST["destination_stop_id"])
        try:
            booking = create_booking(request.user, trip, seat, boarding_stop, destination_stop)
            return redirect("booking_detail", booking.id)
        except ValidationError as e:
            return render(request, "bookings/seat_selection.html", {
                "trip": trip,
                "seats": get_available_seats(trip),
                "error": str(e),
            })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(passenger=request.user).order_by("-created_at")
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, passenger=request.user)
    return render(request, "bookings/booking_detail.html", {"booking": booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, passenger=request.user)
    if booking.trip.status in ("SCHEDULED", "BOARDING") and booking.status == "CONFIRMED":
        booking.status = Booking.Status.CANCELLED
        booking.save()
    return redirect("my_bookings")