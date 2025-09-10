from datetime import timedelta

import pytest
from django.utils import timezone

from meetings.api.serializers import MeetingSerializer


@pytest.mark.django_db
class TestMeetingSerializer:
    def test_valid_data(self, user):
        start = timezone.now().replace(microsecond=0) + timedelta(hours=2)
        end = start + timedelta(hours=1)

        data = {
            "title": "New Meeting",
            "description": "Desc",
            "start_time": start,
            "end_time": end,
            "participants": [user.id],
        }
        serializer = MeetingSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        meeting_obj = serializer.save(created_by=user)
        assert meeting_obj.title == "New Meeting"
        assert user in meeting_obj.participants.all()

    def test_end_time_before_start_invalid(self, user):
        start = timezone.now().replace(microsecond=0)
        end = start - timedelta(minutes=10)

        data = {
            "title": "Invalid Meeting",
            "description": "Desc",
            "start_time": start,
            "end_time": end,
            "participants": [user.id],
        }
        serializer = MeetingSerializer(data=data)
        assert not serializer.is_valid()
        assert "Встреча не может заканчиваться раньше" in str(
            serializer.errors)

    def test_conflicting_meeting_invalid(self, user, meeting):
        start = meeting.start_time + timedelta(minutes=30)
        end = meeting.end_time + timedelta(minutes=30)

        data = {
            "title": "Conflict",
            "description": "Desc",
            "start_time": start,
            "end_time": end,
            "participants": [user.id],
        }
        serializer = MeetingSerializer(data=data)
        assert not serializer.is_valid()
        assert f"У пользователя {user.email}" in str(serializer.errors)

    def test_edit_meeting_no_conflict_with_self(self, user, meeting):
        data = {
            "title": "Updated Title",
            "description": "Updated",
            "start_time": meeting.start_time,
            "end_time": meeting.end_time,
            "participants": [user.id],
        }
        serializer = MeetingSerializer(instance=meeting, data=data)
        assert serializer.is_valid(), serializer.errors
        obj = serializer.save()
        assert obj.title == "Updated Title"

    def test_read_only_fields(self, user):
        start = timezone.now().replace(microsecond=0)
        end = start + timedelta(hours=1)
        data = {
            "title": "Test",
            "description": "Desc",
            "start_time": start,
            "end_time": end,
            "participants": [user.id],
            "id": 999,
            "created_by": 999
        }
        serializer = MeetingSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        obj = serializer.save(created_by=user)
        assert obj.id != 999
        assert obj.created_by == user
