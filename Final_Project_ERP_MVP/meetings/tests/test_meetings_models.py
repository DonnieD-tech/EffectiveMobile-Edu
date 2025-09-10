from datetime import timedelta

import pytest
from django.utils import timezone

from meetings.models import Meeting
from users.models import User


@pytest.mark.django_db
class TestMeetingModel:
    def test_create_meeting(self):
        user = User.objects.create(first_name="creator")
        meeting = Meeting.objects.create(
            title="Team Sync",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            created_by=user,
        )
        assert Meeting.objects.count() == 1
        assert meeting.title == "Team Sync"
        assert meeting.created_by == user

    def test_str_returns_title(self):
        user = User.objects.create(first_name="creator")
        meeting = Meeting.objects.create(
            title="Planning",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            created_by=user,
        )
        assert str(meeting) == "Planning"

    def test_ordering_by_start_time(self):
        user = User.objects.create(first_name="creator")
        m1 = Meeting.objects.create(
            title="Earlier",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            created_by=user,
        )
        m2 = Meeting.objects.create(
            title="Later",
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1),
            created_by=user,
        )
        meetings = list(Meeting.objects.all())
        assert meetings == [m1, m2]

    def test_participants_can_be_added(self):
        creator = User.objects.create(first_name="creator")
        p1 = User.objects.create(
            first_name="user1",
            email="user1@list.ru"
        )
        p2 = User.objects.create(
            first_name="user2",
            email="user2@list.ru"
        )

        meeting = Meeting.objects.create(
            title="Workshop",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=2),
            created_by=creator,
        )
        meeting.participants.add(p1, p2)
        meeting.save()

        assert meeting.participants.count() == 2
        assert p1 in meeting.participants.all()
        assert p2 in meeting.participants.all()

    def test_overlaps_true(self):
        user = User.objects.create(first_name="creator")
        m1 = Meeting.objects.create(
            title="Morning",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=2),
            created_by=user,
        )
        m2 = Meeting.objects.create(
            title="Overlap",
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=3),
            created_by=user,
        )
        assert m1.overlaps(m2) is True
        assert m2.overlaps(m1) is True

    def test_overlaps_false(self):
        user = User.objects.create(first_name="creator")
        m1 = Meeting.objects.create(
            title="Morning",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=2),
            created_by=user,
        )
        m2 = Meeting.objects.create(
            title="Afternoon",
            start_time=timezone.now() + timedelta(hours=3),
            end_time=timezone.now() + timedelta(hours=4),
            created_by=user,
        )
        assert m1.overlaps(m2) is False
        assert m2.overlaps(m1) is False
