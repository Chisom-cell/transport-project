from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        GOVERNMENT_ADMIN = "GOVERNMENT_ADMIN", "Government Admin"
        OPERATOR_ADMIN = "OPERATOR_ADMIN", "Operator Admin"
        DRIVER = "DRIVER", "Driver"
        PASSENGER = "PASSENGER", "Passenger"

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.PASSENGER,
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email