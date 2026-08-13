from django.test import TestCase
from django.contrib.auth import get_user_model

from transport.models import (
    Organization,
    Route,
    Vehicle,
    DriverProfile,
    Trip,
)

from .models import Complaint


User = get_user_model()


class ComplaintModelTest(TestCase):

    def setUp(self):
        # Create passenger
        self.passenger = User.objects.create_user(
            username="passenger1",
            password="testpass123",
        )

        # Create organization
        self.organization = Organization.objects.create(
            name="Abia State Transport",
            organization_type="GOVERNMENT",
        )

        # Create route
        self.route = Route.objects.create(
            name="Aba - Umuahia",
            origin="Aba",
            destination="Umuahia",
        )

        # Create vehicle
        self.vehicle = Vehicle.objects.create(
            organization=self.organization,
            vehicle_code="ABIA-001",
            registration_number="ABC-123",
            vehicle_type="Bus",
            capacity=30,
        )

        # Create driver user
        self.driver_user = User.objects.create_user(
            username="driver1",
            password="testpass123",
        )

        # Create driver profile
        self.driver = DriverProfile.objects.create(
            user=self.driver_user,
            organization=self.organization,
            license_number="LIC-001",
        )

        # Create trip
        self.trip = Trip.objects.create(
            organization=self.organization,
            route=self.route,
            vehicle=self.vehicle,
            driver=self.driver,
            departure_time="2026-08-20 10:00:00",
        )

    def test_complaint_can_be_created(self):

        complaint = Complaint.objects.create(
            passenger=self.passenger,
            trip=self.trip,
            vehicle=self.vehicle,
            category="DRIVER_BEHAVIOUR",
            description="The driver was rude.",
        )

        self.assertEqual(
            complaint.passenger,
            self.passenger,
        )

        self.assertEqual(
            complaint.trip,
            self.trip,
        )

        self.assertEqual(
            complaint.vehicle,
            self.vehicle,
        )

    def test_new_complaint_is_open(self):

        complaint = Complaint.objects.create(
            passenger=self.passenger,
            trip=self.trip,
            vehicle=self.vehicle,
            category="SAFETY",
            description="The bus was not safe.",
        )

        self.assertEqual(
            complaint.status,
            Complaint.Status.OPEN,
        )

    def test_complaint_status_can_change(self):

        complaint = Complaint.objects.create(
            passenger=self.passenger,
            trip=self.trip,
            vehicle=self.vehicle,
            category="SERVICE",
            description="Poor service.",
        )

        complaint.status = Complaint.Status.INVESTIGATING
        complaint.save()

        complaint.refresh_from_db()

        self.assertEqual(
            complaint.status,
            Complaint.Status.INVESTIGATING,
        )

        complaint.status = Complaint.Status.RESOLVED
        complaint.save()

        complaint.refresh_from_db()

        self.assertEqual(
            complaint.status,
            Complaint.Status.RESOLVED,
        )