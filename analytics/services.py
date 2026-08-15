from datetime import datetime, time

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from transport.models import (
    Route,
    BusStop,
    Vehicle,
    Trip,
)


def get_total_routes():
    """Return the total number of routes in the system."""
    return Route.objects.count()


def get_active_routes():
    """Return the number of active routes."""
    return Route.objects.filter(
        is_active=True
    ).count()


def get_total_bus_stops():
    """Return the total number of bus stops in the system."""
    return BusStop.objects.count()


def get_active_bus_stops():
    """Return the number of active bus stops."""
    return BusStop.objects.filter(
        is_active=True
    ).count()


def get_total_vehicles():
    """Return the total number of vehicles in the system."""
    return Vehicle.objects.count()


def get_active_vehicles():
    """Return the number of active vehicles."""
    return Vehicle.objects.filter(
        status=Vehicle.Status.ACTIVE
    ).count()


def get_maintenance_vehicles():
    """Return the number of vehicles under maintenance."""
    return Vehicle.objects.filter(
        status=Vehicle.Status.MAINTENANCE
    ).count()


def get_total_trips():
    """Return the total number of trips in the system."""
    return Trip.objects.count()


def get_trips_by_status():
    """Return the number of trips grouped by status."""
    return (
        Trip.objects
        .values("status")
        .annotate(total=Count("id"))
        .order_by("-total")
    )


def get_trips_by_route():
    """Return the number of trips grouped by route."""
    return (
        Trip.objects
        .values(
            "route__name",
            "route__origin",
            "route__destination",
        )
        .annotate(total=Count("id"))
        .order_by("-total")
    )


def get_trips_by_organization():
    """Return the number of trips grouped by organization."""
    return (
        Trip.objects
        .values("organization__name")
        .annotate(total=Count("id"))
        .order_by("-total")
    )


def get_trips_by_date():
    """Return the number of trips grouped by date."""
    return (
        Trip.objects
        .annotate(
            trip_date=TruncDate("departure_time")
        )
        .values("trip_date")
        .annotate(total=Count("id"))
        .order_by("trip_date")
    )


def get_trips_by_date_range(start_date=None, end_date=None):
    """
    Return trips grouped by date within
    a selected date range.
    """

    queryset = Trip.objects.all()

    # Start date
    if start_date:
        start_datetime = timezone.make_aware(
            datetime.combine(
                start_date,
                time.min
            )
        )

        queryset = queryset.filter(
            departure_time__gte=start_datetime
        )

    # End date
    if end_date:
        end_datetime = timezone.make_aware(
            datetime.combine(
                end_date,
                time.max
            )
        )

        queryset = queryset.filter(
            departure_time__lte=end_datetime
        )

    return (
        queryset
        .annotate(
            trip_date=TruncDate("departure_time")
        )
        .values("trip_date")
        .annotate(total=Count("id"))
        .order_by("trip_date")
    )