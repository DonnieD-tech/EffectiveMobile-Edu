import pytest
from rest_framework.exceptions import ValidationError

from teams.api.serializers import (
    TeamCreateSerializer,
    TeamJoinSerializer,
    TeamSerializer,
)
from teams.models import Team
from users.models import User


@pytest.mark.django_db
class TestTeamSerializer:
    def test_team_serializer_members(self, user):
        team = Team.objects.create(
            name="Test Team",
            admin=user
        )
        member = User.objects.create_user(
            email="member@example.com",
            password="password123",
            first_name="Member",
            last_name="User",
            team=team
        )
        serializer = TeamSerializer(instance=team)
        data = serializer.data
        assert data["id"] == team.id
        assert data["name"] == "Test Team"
        assert data["admin"] == str(user)

        member_data = data["members"][0]
        assert member_data["id"] == member.id
        assert member_data["email"] == member.email
        assert member_data["first_name"] == member.first_name
        assert member_data["last_name"] == member.last_name
        assert member_data["role"] == member.role


@pytest.mark.django_db
class TestTeamCreateSerializer:
    def test_create_team_assigns_admin_and_team(self, user):
        data = {"name": "New Team"}
        serializer = TeamCreateSerializer(
            data=data,
            context={
                "request": type(
                    "Req",
                    (),
                    {"user": user}
                )
                ()
            }
        )
        assert serializer.is_valid()
        team = serializer.save()

        assert team.name == "New Team"
        assert team.admin == user

        user.refresh_from_db()
        assert user.team == team


@pytest.mark.django_db
class TestTeamJoinSerializer:
    def test_join_team_success(self, user):
        team = Team.objects.create(
            name="Joinable Team",
            admin=user
        )
        new_user = User.objects.create_user(
            email="new@example.com",
            password="password123",
            first_name="New",
            last_name="User"
        )

        serializer = TeamJoinSerializer(
            data={"invite_code": team.invite_code},
            context={
                "request": type(
                    "Req",
                    (),
                    {"user": new_user}
                )
                ()
            }
        )
        assert serializer.is_valid()
        joined_team = serializer.save()

        assert joined_team == team
        new_user.refresh_from_db()
        assert new_user.team == team

    def test_join_team_invalid_code(self, user):
        new_user = User.objects.create_user(
            email="new2@example.com",
            password="password123",
            first_name="New2",
            last_name="User2"
        )
        serializer = TeamJoinSerializer(
            data={"invite_code": "wrongcode"},
            context={
                "request": type(
                    "Req",
                    (),
                    {"user": new_user}
                )
                ()
            }
        )
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
