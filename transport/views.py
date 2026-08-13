from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages


from .models import Trip, Route, BusStop
from bookings.models import Booking




# Create your views here.




def home(request):
    return render(request, "transport/home.html")

@login_required
def book_trip(request, trip_id):
    trip = get_object_or_404(
        Trip.objects.select_related(
            "route",
            "vehicle",
            "organization",
        ),
        id=trip_id,
        status__in=[
            Trip.Status.SCHEDULED,
            Trip.Status.BOARDING,
        ],
    )

    route_stops = trip.route.route_stops.select_related(
        "bus_stop"
    ).order_by("stop_order")

    if request.method == "POST":
        boarding_stop_id = request.POST.get("boarding_stop")
        destination_stop_id = request.POST.get("destination_stop")

        boarding_stop = get_object_or_404(
            BusStop,
            id=boarding_stop_id,
        )

        destination_stop = get_object_or_404(
            BusStop,
            id=destination_stop_id,
        )

        if boarding_stop == destination_stop:
            messages.error(
                request,
                "Boarding and destination stops cannot be the same.",
            )

        else:
            booking = Booking.objects.create(
                passenger=request.user,
                trip=trip,
                boarding_stop=boarding_stop,
                destination_stop=destination_stop,
                status=Booking.Status.CONFIRMED,
            )

            messages.success(
                request,
                "Your trip has been booked successfully!",
            )

            return redirect(
                "transport:booking_success",
                booking_id=booking.id,
            )

    return render(
        request,
        "transport/book_trip.html",
        {
            "trip": trip,
            "route_stops": route_stops,
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
    routes = Route.objects.filter(
        is_active=True
    ).prefetch_related(
        "route_stops__bus_stop"
    )

    return render(
        request,
        "transport/routes.html",
        {
            "routes": routes,
        }
    )
    
    
def trips(request, route_id):
    route = get_object_or_404(
        Route,
        id=route_id,
        is_active=True,
    )

    trips = Trip.objects.filter(
        route=route,
        status__in=[
            Trip.Status.SCHEDULED,
            Trip.Status.BOARDING,
        ],
    ).select_related(
        "organization",
        "vehicle",
        "driver",
    ).order_by(
        "departure_time"
    )

    return render(
        request,
        "transport/trips.html",
        {
            "route": route,
            "trips": trips,
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
    
def trip_detail(request, trip_id):
    trip = get_object_or_404(
        Trip.objects.select_related(
            "route",
            "vehicle",
            "organization",
            "driver",
        ),
        id=trip_id,
        status__in=[
            Trip.Status.SCHEDULED,
            Trip.Status.BOARDING,
        ],
    )

    return render(
        request,
        "transport/trip_detail.html",
        {
            "trip": trip,
        },
    )