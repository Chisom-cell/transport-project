from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path(
        "trips/<int:trip_id>/seats/",
        views.seat_selection,
        name="seat_selection"
    ),

    path(
        "trips/<int:trip_id>/confirm/",
        views.confirm_booking,
        name="confirm_booking"
    ),

    path(
        "my-bookings/",
        views.my_bookings,
        name="my_bookings"
    ),

    path(
        "bookings/<int:booking_id>/",
        views.booking_detail,
        name="booking_detail"
    ),

    path(
        "bookings/<int:booking_id>/cancel/",
        views.cancel_booking,
        name="cancel_booking"
    ),
]