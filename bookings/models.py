from django.db import models
from django.contrib.auth.models import User
from transport.models import Trip, Seat, BusStop


class Booking(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    passenger = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    seat = models.ForeignKey(
        Seat,
        on_delete=models.PROTECT,
        related_name="bookings"
    )

    boarding_stop = models.ForeignKey(
        BusStop,
        on_delete=models.PROTECT,
        related_name="boarding_bookings"
    )

    destination_stop = models.ForeignKey(
        BusStop,
        on_delete=models.PROTECT,
        related_name="destination_bookings"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.passenger.username} - {self.trip} - Seat {self.seat}"