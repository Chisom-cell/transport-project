from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    # Seat selection for a particular trip
    path(
        "trips/<int:trip_id>/seats/",
        views.seat_selection,
        name="seat_selection",
    ),

    # Confirm a booking
    path(
        "trips/<int:trip_id>/confirm/",
        views.confirm_booking,
        name="confirm_booking",
    ),

    # User's bookings
    path(
        "",
        views.my_bookings,
        name="my_bookings",
    ),

    # Booking details
    path(
        "<int:booking_id>/",
        views.booking_detail,
        name="booking_detail",
    ),

    # Cancel booking
    path(
        "<int:booking_id>/cancel/",
        views.cancel_booking,
        name="cancel_booking",
    ),
]