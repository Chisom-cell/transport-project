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


# =========================================================
# ROUTE ANALYTICS
# =========================================================

def get_total_routes():
    """Return the total number of routes."""
    return Route.objects.count()


def get_active_routes():
    """Return the number of active routes."""
    return Route.objects.filter(
        is_active=True
    ).count()


# =========================================================
# BUS STOP ANALYTICS
# =========================================================

def get_total_bus_stops():
    """Return the total number of bus stops."""
    return BusStop.objects.count()


def get_active_bus_stops():
    """Return the number of active bus stops."""
    return BusStop.objects.filter(
        is_active=True
    ).count()


# =========================================================
# VEHICLE ANALYTICS
# =========================================================

def get_total_vehicles():
    """Return the total number of vehicles."""
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


# =========================================================
# TRIP ANALYTICS
# =========================================================

def get_total_trips():
    """Return the total number of trips."""
    return Trip.objects.count()


def get_trips_by_status():
    """Return trips grouped by status."""
    return (
        Trip.objects
        .values("status")
        .annotate(total=Count("id"))
        .order_by("-total")
    )


def get_trips_by_route():
    """Return trips grouped by route."""
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
    """Return trips grouped by organization."""
    return (
        Trip.objects
        .values("organization__name")
        .annotate(total=Count("id"))
        .order_by("-total")
    )


def get_trips_by_date():
    """Return trips grouped by date."""
    return (
        Trip.objects
        .annotate(
            trip_date=TruncDate(
                "departure_time"
            )
        )
        .values("trip_date")
        .annotate(
            total=Count("id")
        )
        .order_by("trip_date")
    )


# =========================================================
# DATE RANGE
# =========================================================

def get_trips_queryset_by_date_range(
    start_date=None,
    end_date=None,
):
    """
    Return a Trip queryset filtered by
    the selected date range.
    """

    queryset = Trip.objects.all()

    if start_date:

        start_datetime = timezone.make_aware(
            datetime.combine(
                start_date,
                time.min,
            )
        )

        queryset = queryset.filter(
            departure_time__gte=start_datetime
        )

    if end_date:

        end_datetime = timezone.make_aware(
            datetime.combine(
                end_date,
                time.max,
            )
        )

        queryset = queryset.filter(
            departure_time__lte=end_datetime
        )

    return queryset


# =========================================================
# FILTERED TRIP ANALYTICS
# =========================================================

def get_trips_by_status_range(
    start_date=None,
    end_date=None,
):
    """Return trips by status within a date range."""

    queryset = get_trips_queryset_by_date_range(
        start_date,
        end_date,
    )

    return (
        queryset
        .values("status")
        .annotate(total=Count("id"))
        .order_by("-total")
    )


def get_trips_by_route_range(
    start_date=None,
    end_date=None,
):
    """Return trips by route within a date range."""

    queryset = get_trips_queryset_by_date_range(
        start_date,
        end_date,
    )

    return (
        queryset
        .values(
            "route__name",
            "route__origin",
            "route__destination",
        )
        .annotate(total=Count("id"))
        .order_by("-total")
    )


def get_trips_by_organization_range(
    start_date=None,
    end_date=None,
):
    """Return trips by organization within a date range."""

    queryset = get_trips_queryset_by_date_range(
        start_date,
        end_date,
    )

    return (
        queryset
        .values("organization__name")
        .annotate(total=Count("id"))
        .order_by("-total")
    )


def get_trips_by_date_range(
    start_date=None,
    end_date=None,
):
    """Return trips grouped by date within a date range."""

    queryset = get_trips_queryset_by_date_range(
        start_date,
        end_date,
    )

    return (
        queryset
        .annotate(
            trip_date=TruncDate(
                "departure_time"
            )
        )
        .values("trip_date")
        .annotate(
            total=Count("id")
        )
        .order_by("trip_date")
    )