from django.contrib.auth.models import AbstractUser
from django.db import models

from transport.models import Organization


class User(AbstractUser):

    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        GOVERNMENT_ADMIN = "GOVERNMENT_ADMIN", "Government Admin"
        OPERATOR_ADMIN = "OPERATOR_ADMIN", "Operator Admin"
        DRIVER = "DRIVER", "Driver"
        PASSENGER = "PASSENGER", "Passenger"

    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.PASSENGER,
    )

    # Organization the user belongs to.
    # Super Admins may not belong to an organization.
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True,
    )

    # Verification identification fields
    nin = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        verbose_name="NIN",
    )

    abssin = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        verbose_name="ABSSIN",
    )

    is_verified = models.BooleanField(
        default=False,
        help_text=(
            "Designates whether the user's NIN/ABSSIN "
            "has been verified."
        ),
    )

    def __str__(self):
        return (
            f"{self.email} "
            f"({self.get_role_display()})"
        )