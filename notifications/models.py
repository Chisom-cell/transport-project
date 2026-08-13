from django.conf import settings
from django.db import models


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        BOOKING_CONFIRMED = "BOOKING_CONFIRMED", "Booking Confirmed"
        BOOKING_CANCELLED = "BOOKING_CANCELLED", "Booking Cancelled"
        TRIP_BOARDING = "TRIP_BOARDING", "Trip Boarding"
        TRIP_DEPARTED = "TRIP_DEPARTED", "Trip Departed"
        BUS_APPROACHING = "BUS_APPROACHING", "Bus Approaching"
        GOVERNMENT_ALERT = "GOVERNMENT_ALERT", "Government Alert"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.title}"