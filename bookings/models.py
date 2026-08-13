from django.conf import settings
from django.db import models

from transport.models import Trip, BusStop


class Booking(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    boarding_stop = models.ForeignKey(
        BusStop,
        on_delete=models.PROTECT,
        related_name="boarding_bookings",
    )

    destination_stop = models.ForeignKey(
        BusStop,
        on_delete=models.PROTECT,
        related_name="destination_bookings",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return (
            f"{self.passenger.username} - "
            f"{self.trip}"
        )