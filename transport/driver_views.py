from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import role_required
from bookings.models import Booking

from .models import Trip, DriverProfile


# =========================================================
# DRIVER DASHBOARD
# =========================================================

@login_required
@role_required("DRIVER")
def driver_dashboard(request):

    driver_profile = get_object_or_404(
        DriverProfile,
        user=request.user,
        is_active=True,
    )

    today = timezone.localdate()

    todays_trip = (
        Trip.objects
        .filter(
            driver=driver_profile,
            departure_time__date=today,
        )
        .select_related(
            "route",
            "vehicle",
            "organization",
            "current_stop",
        )
        .order_by("departure_time")
        .first()
    )

    passenger_count = 0

    if todays_trip:
        passenger_count = (
            Booking.objects
            .filter(
                trip=todays_trip,
                status=Booking.Status.CONFIRMED,
            )
            .count()
        )

    return render(
        request,
        "dashboards/driver.html",
        {
            "todays_trip": todays_trip,
            "passenger_count": passenger_count,
        },
    )


# =========================================================
# DRIVER TRIPS
# =========================================================

@login_required
@role_required("DRIVER")
def driver_trips(request):

    driver_profile = get_object_or_404(
        DriverProfile,
        user=request.user,
        is_active=True,
    )

    trips = (
        Trip.objects
        .filter(
            driver=driver_profile,
        )
        .select_related(
            "route",
            "vehicle",
            "organization",
            "current_stop",
        )
        .order_by("-departure_time")
    )

    return render(
        request,
        "transport/driver_trips.html",
        {
            "trips": trips,
        },
    )


# =========================================================
# DRIVER TRIP DETAIL
# =========================================================

@login_required
@role_required("DRIVER")
def driver_trip_detail(request, trip_id):

    driver_profile = get_object_or_404(
        DriverProfile,
        user=request.user,
        is_active=True,
    )

    trip = get_object_or_404(
        Trip.objects.select_related(
            "route",
            "vehicle",
            "organization",
            "driver",
            "current_stop",
        ),
        id=trip_id,
        driver=driver_profile,
    )

    passengers = (
        Booking.objects
        .filter(
            trip=trip,
            status=Booking.Status.CONFIRMED,
        )
        .select_related(
            "passenger",
            "boarding_stop",
            "destination_stop",
            "seat",
        )
        .order_by(
            "seat__seat_number",
            "created_at",
        )
    )

    return render(
        request,
        "transport/driver_trip_detail.html",
        {
            "trip": trip,
            "passengers": passengers,
        },
    )


# =========================================================
# UPDATE TRIP STATUS
# =========================================================

@login_required
@role_required("DRIVER")
def driver_update_trip_status(request, trip_id):

    driver_profile = get_object_or_404(
        DriverProfile,
        user=request.user,
        is_active=True,
    )

    trip = get_object_or_404(
        Trip,
        id=trip_id,
        driver=driver_profile,
    )

    if request.method != "POST":
        return redirect(
            "transport:driver_trip_detail",
            trip_id=trip.id,
        )

    requested_status = request.POST.get("status")

    valid_transitions = {
        Trip.Status.SCHEDULED: Trip.Status.BOARDING,
        Trip.Status.BOARDING: Trip.Status.DEPARTED,
        Trip.Status.DEPARTED: Trip.Status.IN_TRANSIT,
        Trip.Status.IN_TRANSIT: Trip.Status.ARRIVED,
    }

    expected_next_status = valid_transitions.get(trip.status)

    if requested_status != expected_next_status:

        messages.error(
            request,
            "Invalid status transition.",
        )

        return redirect(
            "transport:driver_trip_detail",
            trip_id=trip.id,
        )

    trip.status = requested_status

    trip.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        f"Trip status updated to "
        f"{trip.get_status_display()}.",
    )

    return redirect(
        "transport:driver_trip_detail",
        trip_id=trip.id,
    )


# =========================================================
# DRIVER VEHICLE
# =========================================================

@login_required
@role_required("DRIVER")
def driver_vehicle(request):

    driver_profile = get_object_or_404(
        DriverProfile,
        user=request.user,
        is_active=True,
    )

    trip = (
        Trip.objects
        .filter(
            driver=driver_profile,
            departure_time__date=timezone.localdate(),
        )
        .select_related(
            "vehicle",
            "organization",
        )
        .order_by("departure_time")
        .first()
    )

    vehicle = trip.vehicle if trip else None

    return render(
        request,
        "transport/driver_vehicle.html",
        {
            "vehicle": vehicle,
            "trip": trip,
        },
    )