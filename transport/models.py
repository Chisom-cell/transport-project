from django.conf import settings
from django.db import models


class Organization(models.Model):
    class OrganizationType(models.TextChoices):
        GOVERNMENT = "GOVERNMENT", "Government"
        PRIVATE = "PRIVATE", "Private"

    name = models.CharField(max_length=150)

    organization_type = models.CharField(
        max_length=20,
        choices=OrganizationType.choices,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class BusStop(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Route(models.Model):
    name = models.CharField(max_length=200)
    origin = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class RouteStop(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="route_stops",
    )

    bus_stop = models.ForeignKey(
        BusStop,
        on_delete=models.PROTECT,
        related_name="route_stops",
    )

    stop_order = models.PositiveIntegerField()

    distance_from_origin_km = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    class Meta:
        ordering = ["stop_order"]

        constraints = [
            models.UniqueConstraint(
                fields=["route", "stop_order"],
                name="unique_route_stop_order",
            ),
        ]

    def __str__(self):
        return f"{self.route.name} - {self.bus_stop.name}"
            
        
        
class Vehicle(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        MAINTENANCE = "MAINTENANCE", "Maintenance"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="vehicles",
    )

    vehicle_code = models.CharField(
        max_length=50,
        unique=True,
    )

    registration_number = models.CharField(
        max_length=50,
        unique=True,
    )

    vehicle_type = models.CharField(
        max_length=80,
    )

    capacity = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    
    maintenance_note = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vehicle_code
    


class Seat(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="seats",
    )

    seat_number = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vehicle", "seat_number"],
                name="unique_vehicle_seat",
            ),
        ]

        ordering = ["seat_number"]

    def __str__(self):
        return f"{self.vehicle.vehicle_code} - Seat {self.seat_number}"
    


class DriverProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="driver_profile",
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="drivers",
    )

    license_number = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
class Trip(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        BOARDING = "BOARDING", "Boarding"
        DEPARTED = "DEPARTED", "Departed"
        IN_TRANSIT = "IN_TRANSIT", "In Transit"
        ARRIVED = "ARRIVED", "Arrived"
        CANCELLED = "CANCELLED", "Cancelled"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="trips",
    )

    route = models.ForeignKey(
        Route,
        on_delete=models.PROTECT,
        related_name="trips",
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="trips",
    )

    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.PROTECT,
        related_name="trips",
    )

    departure_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )

    current_stop = models.ForeignKey(
        BusStop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_trips",
    )

    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def total_capacity(self):
        return self.vehicle.capacity
    
    @property
    def booked_capacity(self):
        return self.bookings.filter(
            status="CONFIRMED"
        ).count()

    @property
    def available_capacity(self):
        return max(
            self.total_capacity - self.booked_capacity,
            0
        )

    def __str__(self):
        return f"{self.route.name} - {self.departure_time:%Y-%m-%d %H:%M}"
    
class FareBand(models.Model):
    min_distance_km = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    
    max_distance_km = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    is_active = models.BooleanField(
        default=True,
    )
    
    created_at = models.DateTimeField(
      auto_now_add=True,  
    )
    
    class Meta:
        ordering = ["min_distance_km"]
        
    def __str__ (self):
        return(
            f"{self.min_distance_km} - "
            f"{self.max_distance_km} - "
            f"₦{self.amount}"
        )