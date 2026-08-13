from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "passenger",
        "trip",
        "seat",
        "boarding_stop",
        "destination_stop",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "passenger__username",
        "passenger__email",
    )

    ordering = (
        "-created_at",
    )