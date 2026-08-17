from django.urls import path

from . import views
from . import driver_views


app_name = "transport"


urlpatterns = [

    # =====================================================
    # PUBLIC TRANSPORT PAGES
    # =====================================================

    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "routes/",
        views.routes,
        name="routes",
    ),

    path(
        "routes/<int:route_id>/",
        views.route_detail,
        name="route_detail",
    ),

    path(
        "routes/<int:route_id>/trips/",
        views.trips,
        name="trips",
    ),

    path(
        "trips/<int:trip_id>/",
        views.trip_detail,
        name="trip_detail",
    ),


    # =====================================================
    # BOOKING
    # =====================================================

    path(
        "book/<int:trip_id>/",
        views.book_trip,
        name="book_trip",
    ),

    path(
        "booking/success/<int:booking_id>/",
        views.booking_success,
        name="booking_success",
    ),


    # =====================================================
    # DRIVER DASHBOARD
    # =====================================================

    path(
        "driver/",
        driver_views.driver_dashboard,
        name="driver_dashboard",
    ),

    path(
        "driver/trips/",
        driver_views.driver_trips,
        name="driver_trips",
    ),

    path(
        "driver/trips/<int:trip_id>/",
        driver_views.driver_trip_detail,
        name="driver_trip_detail",
    ),


    # =====================================================
    # DRIVER TRIP STATUS
    # =====================================================

    path(
        "driver/trips/<int:trip_id>/update-status/",
        driver_views.driver_update_trip_status,
        name="update_trip_status",
    ),


    # =====================================================
    # DRIVER VEHICLE
    # =====================================================

    path(
        "driver/vehicle/",
        driver_views.driver_vehicle,
        name="driver_vehicle",
    ),
]