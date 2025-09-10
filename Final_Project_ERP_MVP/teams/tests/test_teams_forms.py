import pytest

from teams.forms import AddMemberForm, JoinTeamForm, TeamCreateForm
from users.models import User


@pytest.mark.django_db
def test_join_team_form_valid():
    form = JoinTeamForm(data={"invite_code": "123456789012"})
    assert form.is_valid()
    assert form.cleaned_data["invite_code"] == "123456789012"


@pytest.mark.django_db
def test_join_team_form_invalid():
    form = JoinTeamForm(data={"invite_code": ""})
    assert not form.is_valid()
    assert "invite_code" in form.errors


@pytest.mark.django_db
def test_team_create_form(user):
    form = TeamCreateForm(data={"name": "New Team"})
    assert form.is_valid()
    team = form.save(commit=False)
    team.admin = user
    team.save()
    assert team.id is not None
    assert team.name == "New Team"


@pytest.mark.django_db
def test_add_member_form_label_from_instance(user, team):
    member_with_team = User.objects.create_user(
        email="member@example.com",
        password="password123",
        first_name="Member",
        last_name="User",
        team=team,
        role=User.Role.USER
    )
    member_no_team = User.objects.create_user(
        email="alone@example.com",
        password="password123",
        first_name="Alone",
        last_name="User",
        role=User.Role.USER
    )

    form = AddMemberForm()
    label_with_team = form.fields["user"].label_from_instance(member_with_team)
    label_no_team = form.fields["user"].label_from_instance(member_no_team)

    assert (f"{member_with_team.first_name} {member_with_team.last_name}"
            f" ({team.name} - {member_with_team.get_role_display()})") == label_with_team
    assert (f"{member_no_team.first_name} {member_no_team.last_name}"
            f" ({member_no_team.get_role_display()})") == label_no_team
