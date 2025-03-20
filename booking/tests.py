from datetime import datetime

from django.utils.timezone import make_aware
from rest_framework.test import APITestCase
from rest_framework import status
from booking.models import Booking, MemberInfo, Inventory
from django.urls import reverse


class BookingAPITestCase(APITestCase):
    def setUp(self):
        self.member = MemberInfo.objects.create(
            name="John",
            surname="Doe",
            booking_count=0,
            date_joined=make_aware(datetime.strptime("01/01/2024", "%d/%m/%Y"))  # Fixing date format
        )
        self.item = Inventory.objects.create(
            title="Bali Trip",
            description="Luxury trip to Bali",
            remaining_count=5,
            expiration_date=datetime.strptime("19/11/2030", "%d/%m/%Y").date()  # Fixing date format
        )
        self.booking_url = reverse("booking-api")  # Define this name in urls.py

    def test_successful_booking(self):
        """Test successful booking creation when inventory is available."""
        response = self.client.post(self.booking_url, {
            "member": self.member.id,
            "item": self.item.id,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_limit_exceeded(self):
        """Test failure when user exceeds max allowed bookings."""
        # Create 1 booking first
        Booking.objects.create(member=self.member, item=self.item)

        response = self.client.post(self.booking_url, {
            "member": self.member.id,
            "item": self.item.id,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Maximum bookings allowed are", response.data["member"][0])

    def test_booking_when_inventory_unavailable(self):
        """Test failure when item has no remaining inventory."""
        self.item.remaining_count = 0
        self.item.save()

        response = self.client.post(self.booking_url, {
            "member": self.member.id,
            "item": self.item.id,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Inventory is not available for the selected item.", response.data["item"][0])


class CancelBookingAPITestCase(APITestCase):
    def setUp(self):
        self.member = MemberInfo.objects.create(
            name="John",
            surname="Doe",
            booking_count=0,
            date_joined=make_aware(datetime.strptime("01/01/2024", "%d/%m/%Y"))  # Fixing date format
        )
        self.other_member = MemberInfo.objects.create(
            name="Jane",
            surname="Dae",
            booking_count=0,
            date_joined=make_aware(datetime.strptime("01/01/2025", "%d/%m/%Y"))  # Fixing date format
        )
        self.item = Inventory.objects.create(
            title="Bali Trip",
            description="Luxury trip to Bali",
            remaining_count=5,
            expiration_date=datetime.strptime("19/11/2030", "%d/%m/%Y").date()  # Fixing date format
        )
        self.booking = Booking.objects.create(member=self.member, item=self.item)
        self.cancel_url = reverse("cancel-booking-api")  # Define this name in urls.py

    def test_successful_cancellation(self):
        """Test successful cancellation of a booking."""
        response = self.client.post(self.cancel_url, {
            "member": self.member.id,
            "booking": self.booking.id,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.STATUS_CANCELLED)

    def test_cannot_cancel_other_members_booking(self):
        """Test failure when trying to cancel someone else's booking."""
        response = self.client.post(self.cancel_url, {
            "member": self.other_member.id,
            "booking": self.booking.id,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This Booking does not belong", response.data["non_field_errors"][0])

    def test_cannot_cancel_already_cancelled_booking(self):
        """Test failure when trying to cancel a booking that is already cancelled."""
        self.booking.status = Booking.STATUS_CANCELLED
        self.booking.save()

        response = self.client.post(self.cancel_url, {
            "member": self.member.id,
            "booking": self.booking.id,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This Booking has already been cancelled.", response.data["non_field_errors"][0])
