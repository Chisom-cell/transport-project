from django.contrib import admin

from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "passenger",
        "trip",
        "vehicle",
        "category",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "created_at",
    )

    search_fields = (
        "passenger__username",
        "passenger__email",
        "category",
        "description",
        "vehicle__vehicle_code",
        "vehicle__registration_number",
    )

    readonly_fields = (
        "created_at",
        # "updated_at",
    )