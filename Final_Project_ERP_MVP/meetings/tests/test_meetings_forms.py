from datetime import timedelta

import pytest
from django.utils import timezone

from meetings.forms import MeetingForm
from meetings.models import Meeting
from users.models import User


@pytest.mark.django_db
class TestMeetingForm:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="u1@example.com", password="pass",
            first_name="U1", last_name="L1"
        )
        self.start = timezone.now().replace(microsecond=0)
        self.end = self.start + timedelta(hours=1)

    def test_valid_form(self):
        form = MeetingForm(data={
            "title": "Valid Meeting",
            "description": "Desc",
            "start_time": self.start,
            "end_time": self.end,
            "participants": [self.user.id],
        })
        assert form.is_valid(), form.errors

    def test_end_time_before_start_time_invalid(self):
        form = MeetingForm(data={
            "title": "Invalid Meeting",
            "description": "Desc",
            "start_time": self.start,
            "end_time": self.start - timedelta(minutes=10),
            "participants": [self.user.id],
        })
        assert not form.is_valid()
        assert "Встреча не может заканчиваться раньше" in str(form.errors)

    def test_conflict_with_existing_meeting_invalid(self):
        Meeting.objects.create(
            title="Existing",
            description="Old",
            start_time=self.start,
            end_time=self.end,
            created_by=self.user
        ).participants.add(self.user)

        form = MeetingForm(data={
            "title": "Conflict",
            "description": "Desc",
            "start_time": self.start + timedelta(minutes=30),
            "end_time": self.end + timedelta(minutes=30),
            "participants": [self.user.id],
        })
        assert not form.is_valid()
        assert "пересекающаяся с этим временем" in str(form.errors)

    def test_no_conflict_when_adjacent_start(self):
        Meeting.objects.create(
            title="Existing",
            description="Old",
            start_time=self.start,
            end_time=self.end,
            created_by=self.user
        ).participants.add(self.user)

        form = MeetingForm(data={
            "title": "No conflict",
            "description": "Desc",
            "start_time": self.end,
            "end_time": self.end + timedelta(hours=1),
            "participants": [self.user.id],
        })
        assert form.is_valid(), form.errors

    def test_no_conflict_when_adjacent_end(self):
        Meeting.objects.create(
            title="Existing",
            description="Old",
            start_time=self.start,
            end_time=self.end,
            created_by=self.user
        ).participants.add(self.user)

        form = MeetingForm(data={
            "title": "No conflict",
            "description": "Desc",
            "start_time": self.start - timedelta(hours=1),
            "end_time": self.start,
            "participants": [self.user.id],
        })
        assert form.is_valid(), form.errors

    def test_edit_meeting_does_not_conflict_with_itself(self):
        meeting = Meeting.objects.create(
            title="Edit me",
            description="Old",
            start_time=self.start,
            end_time=self.end,
            created_by=self.user
        )
        meeting.participants.add(self.user)

        form = MeetingForm(
            data={
                "title": "Edit me",
                "description": "Updated",
                "start_time": self.start,
                "end_time": self.end,
                "participants": [self.user.id],
            },
            instance=meeting
        )
        assert form.is_valid(), form.errors
