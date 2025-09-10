from datetime import timedelta

import pytest
from django.utils import timezone

from meetings.models import Meeting
from users.models import User


@pytest.fixture
def user():
    return User.objects.create_user(
        email="user@example.com",
        password="pass",
        first_name="First",
        last_name="Last"
    )


@pytest.fixture
def manager():
    return User.objects.create_user(
        email="manager@example.com",
        password="pass",
        first_name="Manager",
        last_name="M",
        role=User.Role.MANAGER
    )


@pytest.fixture
def meeting(user):
    m = Meeting.objects.create(
        title="Existing Meeting",
        description="Old",
        start_time=timezone.now().replace(microsecond=0),
        end_time=timezone.now().replace(microsecond=0) + timedelta(hours=1),
        created_by=user
    )
    m.participants.add(user)
    return m
