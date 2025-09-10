from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from meetings.models import Meeting
from users.models import User


@pytest.mark.django_db
class TestMeetingAPI:
    def test_list_meetings_authenticated(self, user, meeting):
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("meeting_list_create")
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == meeting.id

    def test_list_meetings_unauthenticated(self):
        client = APIClient()
        url = reverse("meeting_list_create")
        response = client.get(url)
        assert response.status_code == 401

    def test_create_meeting_valid(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("meeting_list_create")
        start = timezone.now().replace(microsecond=0) + timedelta(hours=2)
        end = start + timedelta(hours=1)
        data = {
            "title": "New Meeting",
            "description": "Desc",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "participants": [user.id],
        }
        response = client.post(url, data, format="json")
        assert response.status_code == 201
        assert response.data["title"] == "New Meeting"
        assert response.data["created_by"] == user.id

    def test_create_meeting_invalid(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("meeting_list_create")
        start = timezone.now().replace(microsecond=0)
        end = start - timedelta(minutes=10)
        data = {
            "title": "Invalid",
            "description": "Desc",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "participants": [user.id],
        }
        response = client.post(url, data, format="json")
        assert response.status_code == 400
        assert "Встреча не может заканчиваться раньше" in str(response.data)

    def test_retrieve_meeting(self, user, meeting):
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("meeting_detail_delete", args=[meeting.id])
        response = client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == meeting.id

    def test_delete_meeting_by_creator(self, user, meeting):
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("meeting_detail_delete", args=[meeting.id])
        response = client.delete(url)
        assert response.status_code == 204
        assert not Meeting.objects.filter(id=meeting.id).exists()

    def test_delete_meeting_by_manager(self, manager, meeting):
        client = APIClient()
        client.force_authenticate(user=manager)
        url = reverse("meeting_detail_delete", args=[meeting.id])
        response = client.delete(url)
        assert response.status_code == 204
        assert not Meeting.objects.filter(id=meeting.id).exists()

    def test_delete_meeting_forbidden(self, user):
        other_user = User.objects.create_user(
            email="other@example.com", password="pass",
            first_name="Other", last_name="User"
        )
        meeting = Meeting.objects.create(
            title="Other Meeting",
            description="Desc",
            start_time=timezone.now().replace(
                microsecond=0),
            end_time=timezone.now().replace(
                microsecond=0) +
            timedelta(
                hours=1),
            created_by=other_user)
        meeting.participants.add(other_user)

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("meeting_detail_delete", args=[meeting.id])
        response = client.delete(url)
        assert response.status_code == 403
