from django.conf import settings
from django.db import models
from transport.models import Trip, Vehicle


class Complaint(models.Model):

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        INVESTIGATING = "INVESTIGATING", "Investigating"
        RESOLVED = "RESOLVED", "Resolved"

    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="complaints"
    )

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="complaints"
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="complaints"
    )

    category = models.CharField(max_length=100)

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.passenger}"
    
class Category(models.TextChoices):
    DRIVER = "DRIVER", "Driver behavior"
    VEHICLE = "VEHICLE", "Vehicle condition"
    FARE = "FARE", "Overcharging"
    DELAY = "DELAY", "Late departure"
    ROUTE = "ROUTE", "Route issue"
    SAFETY = "SAFETY", "Safety concern"
    BOOKING = "BOOKING", "Booking issue"
    OTHER = "OTHER", "Other"
category = models.CharField(
    max_length=20,
    choices=Category.choices
)