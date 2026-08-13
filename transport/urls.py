from django.urls import path

from . import views

app_name = "transport"

urlpatterns = [
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