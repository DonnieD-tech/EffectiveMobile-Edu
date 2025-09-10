import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from teams.models import Team
from users.models import User


@pytest.mark.django_db
class TestJoinTeamView:
    def test_get_join_team_page(self, auth_client):
        url = reverse('join_team')
        response = auth_client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_post_join_valid_code(self, auth_client, user, team):
        url = reverse('join_team')
        response = auth_client.post(
            url,
            {"invite_code": team.invite_code}
        )
        user.refresh_from_db()
        assert response.status_code == 302
        assert user.team == team
        assert user.role == User.Role.USER

    def test_post_join_invalid_code(self, auth_client):
        url = reverse('join_team')
        response = auth_client.post(
            url,
            {"invite_code": "wrongcode"}
        )
        assert response.status_code == 200
        messages = [m.message for m in get_messages(response.wsgi_request)]
        assert "Неверный код приглашения" in messages


@pytest.mark.django_db
class TestTeamCreateView:
    def test_get_create_team_page(self, auth_client):
        url = reverse('team_create')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_post_create_team(self, auth_client, user):
        url = reverse('team_create')
        response = auth_client.post(
            url, {"name": "New Team"}
        )
        team = Team.objects.get(
            name="New Team"
        )
        assert response.status_code == 302
        assert team.admin == user


@pytest.mark.django_db
class TestTeamDetailView:
    def test_team_detail_for_member(self, auth_client, user, team):
        url = reverse(
            'team_detail',
            kwargs={"pk": team.id}
        )
        response = auth_client.get(url)
        assert response.status_code == 200
        assert "members" in response.context
        assert "tasks" in response.context

    def test_team_detail_for_non_member_redirect(self, auth_client, user):
        team = Team.objects.create(
            name="Other Team",
            admin=user
        )
        url = reverse(
            'team_detail',
            kwargs={"pk": team.id}
        )
        response = auth_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse('join_team')


@pytest.mark.django_db
class TestTeamUpdateView:
    def test_update_team_name(self, auth_client, team):
        url = reverse(
            'team_edit',
            kwargs={"pk": team.id}
        )
        response = auth_client.post(
            url,
            {"name": "Updated Name"}
        )
        team.refresh_from_db()
        assert response.status_code == 302
        assert team.name == "Updated Name"

    def test_add_member(self, auth_client, team, db):
        new_user = User.objects.create_user(
            email="new@example.com",
            password="password123",
            first_name="New",
            last_name="User"
        )
        url = reverse('team_edit', kwargs={"pk": team.id})
        response = auth_client.post(
            url,
            {
                "add_member": "1",
                "user": new_user.id
            }
        )
        new_user.refresh_from_db()
        assert response.status_code == 302
        assert new_user.team == team
        assert new_user.role == User.Role.USER

    @pytest.mark.django_db
    def test_remove_member(self, auth_client, team, user):
        member = User.objects.create_user(
            email="member@example.com",
            password="password123",
            first_name="Member",
            last_name="User",
            team=team,
            role=User.Role.USER
        )

        url = reverse('team_edit', kwargs={"pk": team.id})
        response = auth_client.post(
            url,
            {"remove_member": member.id}
        )
        member.refresh_from_db()

        assert response.status_code == 302
        assert member.team is None
        assert member.role == User.Role.USER


@pytest.mark.django_db
class TestTeamManageRolesView:
    def test_change_member_role(self, auth_client, team, user):
        other_member = User.objects.create_user(
            email="member@example.com",
            password="password123",
            first_name="Other",
            last_name="Member",
            team=team
        )
        url = reverse('team_manage_roles', kwargs={"team_id": team.id})
        response = auth_client.post(
            url,
            {
                "user_id": other_member.id,
                "role": User.Role.ADMIN_TEAM
            }
        )
        other_member.refresh_from_db()
        assert response.status_code == 302
        assert other_member.role == User.Role.ADMIN_TEAM

    def test_cannot_change_own_role(self, auth_client, team, user):
        url = reverse(
            'team_manage_roles',
            kwargs={"team_id": team.id}
        )
        response = auth_client.post(
            url,
            {
                "user_id": user.id,
                "role": User.Role.ADMIN_TEAM
            }
        )
        user.refresh_from_db()
        messages = [m.message for m in get_messages(response.wsgi_request)]
        assert "Вы не можете изменить свою роль" in messages
        assert user.role == User.Role.ADMIN_TEAM


@pytest.mark.django_db
class TestRemoveMemberView:
    def test_admin_can_remove_member(self, auth_client, team, user):
        member = User.objects.create_user(
            email="member@example.com",
            password="password123",
            first_name="Member",
            last_name="User",
            team=team
        )
        url = reverse(
            'team_edit',
            kwargs={"pk": team.id}
        )
        response = auth_client.post(
            url,
            {"remove_member": member.id}
        )

        member.refresh_from_db()
        assert response.status_code == 302
        assert member.team is None
        assert member.role == User.Role.USER

    def test_cannot_remove_admin(self, auth_client, team, user):
        url = reverse(
            'team_edit',
            kwargs={"pk": team.id}
        )
        response = auth_client.post(
            url,
            {"remove_member": user.id}
        )

        messages = [m.message for m in get_messages(response.wsgi_request)]
        assert "Нельзя исключить администратора команды" in messages

        user.refresh_from_db()
        assert user.team == team
        assert user.role == User.Role.ADMIN_TEAM or user.role == User.Role.USER
