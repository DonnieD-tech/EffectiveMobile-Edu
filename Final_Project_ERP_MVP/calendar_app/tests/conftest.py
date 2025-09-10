from datetime import date, datetime, timedelta

import pytest
from django.test import Client
from django.utils import timezone

from meetings.models import Meeting
from tasks.models import Task
from teams.models import Team
from users.models import User


@pytest.fixture
def today():
    return datetime.today().date()


@pytest.fixture
def meeting_today(db, manager, team, today):
    start_time = datetime.combine(
        today, datetime.min.time()) + timedelta(hours=9)
    end_time = datetime.combine(
        today, datetime.min.time()) + timedelta(hours=10)
    return Meeting.objects.create(
        title="Team Meeting",
        start_time=start_time,
        end_time=end_time,
        created_by=manager
    )


@pytest.fixture
def meeting_other_month(db, manager):
    today = date.today()
    if today.month == 12:
        next_month = date(today.year + 1, 1, 1)
    else:
        next_month = date(today.year, today.month + 1, 1)
    start_time = datetime.combine(next_month,
                                  datetime.min.time()) + timedelta(hours=10)
    end_time = start_time + timedelta(hours=1)
    return Meeting.objects.create(
        title="Other Meeting",
        start_time=start_time,
        end_time=end_time,
        created_by=manager
    )


@pytest.fixture
def task(db, manager, team):
    """
    Создаём задачу с deadline на сегодня.
    """
    return Task.objects.create(
        title="Test Task",
        description="Some description",
        created_by=manager,
        team=team,
        deadline=timezone.now()
    )


@pytest.fixture
def manager(db):
    return User.objects.create_user(
        email="manager@example.com",
        password="pass123",
        first_name="Jane",
        last_name="Smith",
        role=User.Role.MANAGER,
    )


@pytest.fixture
def team(db, manager):
    team = Team.objects.create(
        name="Test Team",
        admin=manager,
    )
    manager.team = team
    manager.save()
    return team


@pytest.fixture
def client():
    return Client()
