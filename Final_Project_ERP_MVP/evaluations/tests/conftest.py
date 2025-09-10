import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from evaluations.models import Evaluation
from tasks.models import Task
from teams.models import Team
from users.models import User


@pytest.fixture
def user():
    return User.objects.create_user(
        email="user@example.com",
        password="password123",
        first_name="John",
        last_name="Doe",
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
def employee(db, team):
    return User.objects.create_user(
        email="employee@example.com",
        password="pass123",
        first_name="Employee",
        last_name="User",
        role=User.Role.USER,
        team=team,
    )


@pytest.fixture
def task(db, manager, team):
    return Task.objects.create(
        title="Test Task",
        description="Some description",
        created_by=manager,
        team=team,
        deadline=timezone.now(),
    )


@pytest.fixture
def evaluation(manager, employee, task):
    return Evaluation.objects.create(
        task=task,
        user=employee,
        score=4,
        created_by=manager,
        comment="Хорошая работа"
    )


@pytest.fixture
def api_client():
    return APIClient()
