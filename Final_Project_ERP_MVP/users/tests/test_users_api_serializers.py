import pytest

from teams.models import Team
from users.api.serializers import (
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
)


@pytest.mark.django_db
class TestUserSerializers:
    def test_user_serializer(self, user):
        serializer = UserSerializer(user)
        data = serializer.data
        assert data["id"] == user.id
        assert data["email"] == user.email
        assert data["first_name"] == user.first_name
        assert data["last_name"] == user.last_name
        assert data["role"] == user.role
        assert data["team"] is None

    def test_user_register_serializer(self):
        data = {
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "securepass"
        }
        serializer = UserRegisterSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user.email == data["email"]
        assert user.check_password(data["password"])

    def test_user_register_serializer_invalid_password(self):
        data = {
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "short"
        }
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_user_update_serializer(self, user):
        team = Team.objects.create(name="Team A", admin=user)
        serializer = UserUpdateSerializer(
            user,
            data={
                "first_name": "Updated",
                "last_name": "Name",
                "team": team.id
            }
        )
        assert serializer.is_valid(), serializer.errors
        updated_user = serializer.save()
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"
        assert updated_user.team == team
