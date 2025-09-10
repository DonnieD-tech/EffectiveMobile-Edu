from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from meetings.models import Meeting
from users.models import User


@pytest.mark.django_db
class TestMeetingViews:
    def test_create_view_requires_login(self, client):
        url = reverse('meeting_create')
        response = client.get(url)
        assert response.status_code == 302

    def test_create_meeting_get(self, client):
        user = User.objects.create_user(
            email="u1@example.com", password="pass",
            first_name="U1", last_name="L1"
        )
        client.login(email="u1@example.com", password="pass")
        url = reverse('meeting_create')
        response = client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_create_meeting_post_valid(self, client):
        user = User.objects.create_user(
            email="u1@example.com", password="pass",
            first_name="U1", last_name="L1"
        )
        assert client.login(email="u1@example.com", password="pass")
        url = reverse('meeting_create')

        start = timezone.now().replace(microsecond=0)
        end = start + timedelta(hours=1)

        start_str = start.strftime('%Y-%m-%dT%H:%M')
        end_str = end.strftime('%Y-%m-%dT%H:%M')

        data = {
            "title": "Test Meeting",
            "description": "Desc",
            "start_time": start_str,
            "end_time": end_str,
            "participants": [user.id],
        }

        response = client.post(url, data)
        assert response.status_code == 302
        assert Meeting.objects.filter(title="Test Meeting").exists()

    def test_create_meeting_post_invalid(self, client):
        user = User.objects.create_user(
            email="u1@example.com", password="pass",
            first_name="U1", last_name="L1"
        )
        client.login(email="u1@example.com", password="pass")
        url = reverse('meeting_create')
        data = {
            "title": "Invalid",
            "description": "Bad time",
            "start_time": timezone.now(),
            "end_time": timezone.now() - timedelta(hours=1),
        }
        response = client.post(url, data)
        assert response.status_code == 200
        assert Meeting.objects.count() == 0

    def test_list_requires_login(self, client):
        url = reverse('meeting_list')
        response = client.get(url)
        assert response.status_code == 302

    def test_list_shows_created_meetings(self, client):
        user = User.objects.create_user(
            email="u1@example.com", password="pass",
            first_name="U1", last_name="L1"
        )
        other = User.objects.create_user(
            email="u2@example.com", password="pass",
            first_name="U2", last_name="L2"
        )
        meeting = Meeting.objects.create(
            title="Created Meeting",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            created_by=user,
        )
        client.login(email="u1@example.com", password="pass")
        response = client.get(reverse('meeting_list'))
        assert response.status_code == 200
        assert meeting in response.context["meetings"]

        client.logout()
        client.login(email="u2@example.com", password="pass")
        response2 = client.get(reverse('meeting_list'))
        assert meeting not in response2.context["meetings"]

    def test_list_shows_participating_meetings(self, client):
        creator = User.objects.create_user(
            email="u1@example.com", password="pass",
            first_name="U1", last_name="L1"
        )
        participant = User.objects.create_user(
            email="u2@example.com", password="pass",
            first_name="U2", last_name="L2"
        )
        meeting = Meeting.objects.create(
            title="Participating Meeting",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            created_by=creator,
        )
        meeting.participants.add(participant)
        client.login(email="u2@example.com", password="pass")
        response = client.get(reverse('meeting_list'))
        assert meeting in response.context["meetings"]

    def test_list_ordering(self, client):
        user = User.objects.create_user(
            email="u1@example.com", password="pass",
            first_name="U1", last_name="L1"
        )
        m1 = Meeting.objects.create(
            title="First",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            created_by=user,
        )
        m2 = Meeting.objects.create(
            title="Second",
            start_time=timezone.now() + timedelta(hours=2),
            end_time=timezone.now() + timedelta(hours=3),
            created_by=user,
        )
        client.login(email="u1@example.com", password="pass")
        response = client.get(reverse('meeting_list'))
        meetings = list(response.context["meetings"])
        assert meetings == [m1, m2]

    # ---------- CANCEL ----------
    def test_cancel_requires_login(self, client):
        url = reverse('meeting_cancel', args=[1])
        response = client.get(url)
        assert response.status_code == 302

    def test_cancel_by_creator(self, client):
        user = User.objects.create_user(
            email="u1@example.com", password="pass",
            first_name="U1", last_name="L1"
        )
        meeting = Meeting.objects.create(
            title="Cancelable",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            created_by=user,
        )
        client.login(email="u1@example.com", password="pass")
        url = reverse('meeting_cancel', args=[meeting.pk])
        response = client.post(url)
        assert response.status_code == 302
        assert Meeting.objects.count() == 0

    def test_cancel_not_creator_forbidden(self, client):
        creator = User.objects.create_user(
            email="u1@example.com", password="pass",
            first_name="U1", last_name="L1"
        )
        other = User.objects.create_user(
            email="u2@example.com", password="pass",
            first_name="U2", last_name="L2"
        )
        meeting = Meeting.objects.create(
            title="Protected",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            created_by=creator,
        )
        client.login(email="u2@example.com", password="pass")
        url = reverse('meeting_cancel', args=[meeting.pk])
        response = client.post(url)
        assert response.status_code == 404
        assert Meeting.objects.count() == 1
