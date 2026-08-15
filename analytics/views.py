from datetime import timedelta

from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.shortcuts import render
from django.utils import timezone

from .services import (
    get_total_routes,
    get_active_routes,
    get_total_bus_stops,
    get_active_bus_stops,
    get_total_vehicles,
    get_active_vehicles,
    get_maintenance_vehicles,
    get_total_trips,
    get_trips_by_status_range,
    get_trips_by_route_range,
    get_trips_by_organization_range,
    get_trips_by_date_range,
)


# =========================================================
# ANALYTICS ACCESS
# =========================================================

def is_analytics_user(user):
    """
    Allow only Super Admin and Government Admin
    users to access Analytics.
    """

    return (
        user.is_authenticated
        and user.role in [
            user.Role.SUPER_ADMIN,
            user.Role.GOVERNMENT_ADMIN,
        ]
    )


# =========================================================
# ANALYTICS DASHBOARD
# =========================================================

@login_required
@user_passes_test(is_analytics_user)
def analytics_dashboard(request):

    today = timezone.localdate()

    # -----------------------------------------------------
    # SELECT PERIOD
    # -----------------------------------------------------

    selected_period = request.GET.get(
        "period",
        "month"
    )

    # -----------------------------------------------------
    # TODAY
    # -----------------------------------------------------

    if selected_period == "today":

        start_date = today
        end_date = today

    # -----------------------------------------------------
    # THIS WEEK
    # -----------------------------------------------------

    elif selected_period == "week":

        start_date = (
            today
            - timedelta(
                days=today.weekday()
            )
        )

        end_date = today

    # -----------------------------------------------------
    # THIS MONTH
    # -----------------------------------------------------

    else:

        selected_period = "month"

        start_date = today.replace(
            day=1
        )

        end_date = today

    # -----------------------------------------------------
    # FILTERED ANALYTICS
    # -----------------------------------------------------

    trips_by_status = list(
        get_trips_by_status_range(
            start_date=start_date,
            end_date=end_date,
        )
    )

    trips_by_route = list(
        get_trips_by_route_range(
            start_date=start_date,
            end_date=end_date,
        )
    )

    trips_by_organization = list(
        get_trips_by_organization_range(
            start_date=start_date,
            end_date=end_date,
        )
    )

    trips_by_date = list(
        get_trips_by_date_range(
            start_date=start_date,
            end_date=end_date,
        )
    )

    # -----------------------------------------------------
    # DASHBOARD CONTEXT
    # -----------------------------------------------------

    context = {

        # Routes
        "total_routes": get_total_routes(),
        "active_routes": get_active_routes(),

        # Bus stops
        "total_bus_stops": get_total_bus_stops(),
        "active_bus_stops": get_active_bus_stops(),

        # Vehicles
        "total_vehicles": get_total_vehicles(),
        "active_vehicles": get_active_vehicles(),
        "maintenance_vehicles": (
            get_maintenance_vehicles()
        ),

        # Total trips for selected period
        "total_trips": sum(
            item["total"]
            for item in trips_by_date
        ),

        # Filtered analytics
        "trips_by_status": trips_by_status,
        "trips_by_route": trips_by_route,
        "trips_by_organization": (
            trips_by_organization
        ),
        "trips_by_date": trips_by_date,

        # Filter information
        "selected_period": selected_period,
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(
        request,
        "government/analytics.html",
        context,
    )