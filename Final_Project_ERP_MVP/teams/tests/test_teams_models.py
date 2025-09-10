import pytest

from teams.models import Team
from users.models import User


@pytest.mark.django_db
def test_create_team(user):
    team = Team.objects.create(name="Test Team", admin=user)
    assert team.id is not None
    assert len(team.invite_code) == 12
    assert team.admin == user
    assert str(team) == f"{team.name} ({team.invite_code})"


@pytest.mark.django_db
def test_team_name_unique(user):
    Team.objects.create(
        name="Unique Team",
        admin=user
    )
    with pytest.raises(Exception):
        Team.objects.create(
            name="Unique Team",
            admin=user
        )


@pytest.mark.django_db
def test_invite_code_auto_generated(user):
    team = Team.objects.create(
        name="AutoCode Team",
        admin=user
    )
    assert team.invite_code is not None
    assert len(team.invite_code) == 12


@pytest.mark.django_db
def test_team_members_relation(user):
    team = Team.objects.create(
        name="Team Members",
        admin=user
    )
    member = User.objects.create_user(
        email="member@example.com",
        password="password123",
        first_name="Member",
        last_name="User"
    )
    member.team = team
    member.role = User.Role.USER
    member.save()

    assert member in team.members.all()
    assert member.team == team
