import json
from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Category, Complaint, Hostel, Status, Student


class ComplaintTimestampTests(TestCase):
    def setUp(self):
        self.hostel = Hostel.objects.create(hostel_id=1, name="A Block")
        self.student = Student.objects.create(
            roll="21CS001",
            name="Test Student",
            mail="student@example.com",
            pswd="pass123",
            mobile="9999999999",
            hostel_id=self.hostel,
        )
        self.category = Category.objects.create(cat_id=1, cat_name="Electrical")
        self.status = Status.objects.create(status_name="Pending")

    def test_complaint_details_returns_india_local_time(self):
        complaint = Complaint.objects.create(
            title="Light issue",
            description="Tube light not working",
            cat_id=self.category,
            student_id=self.student,
            hostel_id=self.hostel,
            status_id=self.status,
        )

        complaint.created_date = datetime(2026, 4, 2, 18, 45, tzinfo=timezone.UTC)
        complaint.solved_date = datetime(2026, 4, 2, 20, 15, tzinfo=timezone.UTC)
        complaint.save(update_fields=["created_date", "solved_date"])

        response = self.client.get(f"/complaint_details/{complaint.Complaint_id}/")

        self.assertEqual(response.status_code, 200)
        payload = json.loads(response.content)
        self.assertEqual(payload["created_date"], "April 03, 2026 - 12:15 AM")
        self.assertEqual(payload["solved_date"], "April 03, 2026 - 01:45 AM")
