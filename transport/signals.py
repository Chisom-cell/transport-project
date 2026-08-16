from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Vehicle, Seat


@receiver(post_save, sender=Vehicle)
def generate_vehicle_seats(sender, instance, created, **kwargs):
    """
    Automatically generate seats when a vehicle is created.
    """

    if not created:
        return

    Seat.objects.bulk_create(
        [
            Seat(
                vehicle=instance,
                seat_number=seat_number,
            )
            for seat_number in range(1, instance.capacity + 1)
        ]
    )