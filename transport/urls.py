from django.urls import path
from . import views

app_name = "transport"

urlpatterns = [
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
]