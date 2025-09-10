import pytest
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIClient

from teams.models import Team
from users.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@example.com",
        password="password123",
        first_name="Иван",
        last_name="Иванов"
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
def team(db, user):
    t = Team.objects.create(
        name="Test Team",
        admin=user
    )
    user.team = t
    user.role = User.Role.ADMIN_TEAM
    user.save()
    return t


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
    url = reverse("token_obtain_pair")
    response = client.post(
        url,
        {
            "email": user.email,
            "password": "password123"
        }
    )
    token = response.data["access"]
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    return client
