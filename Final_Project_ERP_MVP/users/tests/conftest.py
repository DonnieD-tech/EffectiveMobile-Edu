import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from evaluations.models import Evaluation
from tasks.models import Task
from teams.models import Team

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@example.com",
        password="password123",
        first_name="Иван",
        last_name="Иванов",
        role=User.Role.USER
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        email="user2@example.com",
        password="password1234",
        first_name="Сергей",
        last_name="Петров",
        role=User.Role.USER
    )


@pytest.fixture
def team(db, manager):
    return Team.objects.create(
        name="Test Team",
        invite_code="TEST123",
        admin=manager
    )


@pytest.fixture
def evaluation(db, user, task):
    return Evaluation.objects.create(
        task=task,
        user=user,
        score=5,
        created_at=timezone.now(),
        created_by=user,
    )


@pytest.fixture
def task(db, user, team):
    return Task.objects.create(
        title="Test Task",
        assignee=user,
        description="Описание задачи",
        status="to_do",
        created_by=user,
        team=team,
        deadline=timezone.now() + timezone.timedelta(days=1),
    )


@pytest.fixture
def manager(db):
    return User.objects.create_user(
        email="manager@example.com",
        password="password123",
        first_name="Мария",
        last_name="Петрова",
        role=User.Role.MANAGER
    )


@pytest.fixture
def admin(db):
    return User.objects.create_user(
        email="admin@example.com",
        password="password123",
        first_name="Сергей",
        last_name="Сидоров",
        role=User.Role.ADMIN_TEAM
    )


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def jwt_client(user):
    client = APIClient()

    url_token = reverse("token_obtain_pair")
    resp_token = client.post(
        url_token,
        {
            "email": user.email,
            "password": "password123"
        }
    )
    access = resp_token.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return client
