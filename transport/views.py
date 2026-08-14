from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from datetime import date
from .forms import BookingForm
from .models import Trip, Route
from bookings.models import Booking
from .services import create_booking
from accounts.forms import PassengerRegistrationForm
from django.urls import reverse

# Create your views here.


def home(request):
    year = date.today().year

    # Handle inline registration submitted from the home page
    if request.method == "POST" and request.POST.get("register_submit"):
        form = PassengerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please log in.")
            return redirect(reverse("accounts:login"))
        else:
            # Render home with form errors
            return render(request, "transport/home.html", {"year": year, "register_form": form})

    # GET
    form = PassengerRegistrationForm()
    return render(request, "transport/home.html", {"year": year, "register_form": form})

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


def routes(request):
    routes = (
        Route.objects
        .filter(is_active=True)
        .prefetch_related("route_stops__bus_stop")
    )

    return render(
        request,
        "transport/routes.html",
        {
            "routes": routes,
        },
    )


def route_detail(request, route_id):
    route = get_object_or_404(
        Route.objects.prefetch_related(
            "route_stops__bus_stop"
        ),
        id=route_id,
        is_active=True,
    )

    return render(
        request,
        "transport/route_detail.html",
        {
            "route": route,
        },
    )


def trips(request, route_id):
    route = get_object_or_404(
        Route,
        id=route_id,
        is_active=True,
    )

    trips = (
        Trip.objects
        .filter(
            route=route,
            status__in=[
                Trip.Status.SCHEDULED,
                Trip.Status.BOARDING,
            ],
        )
        .select_related(
            "organization",
            "vehicle",
            "driver",
        )
        .order_by("departure_time")
    )

    return render(
        request,
        "transport/trips.html",
        {
            "route": route,
            "trips": trips,
        },
    )
    
def trip_detail(request, trip_id):
    trip = get_object_or_404(
        Trip.objects.select_related(
            "route",
            "vehicle",
            "driver",
            "organization",
        ),
        id=trip_id,
    )

    return render(
        request,
        "transport/trip_detail.html",
        {
            "trip": trip,
        },
    )