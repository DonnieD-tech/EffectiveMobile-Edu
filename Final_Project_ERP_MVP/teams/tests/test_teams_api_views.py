import pytest
from rest_framework import status

from teams.models import Team
from users.models import User


@pytest.mark.django_db
class TestTeamAPI:
    def test_create_team(self, jwt_client, user):
        url = "/api/teams/"
        data = {"name": "New API Team"}
        response = jwt_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        team = Team.objects.get(name="New API Team")
        assert team.admin == user
        user.refresh_from_db()
        assert user.team == team

    def test_get_team_detail(self, jwt_client, user):
        team = Team.objects.create(name="Detail Team", admin=user)
        url = f"/api/teams/{team.id}/"
        response = jwt_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Detail Team"
        assert response.data["admin"] == str(user)

    def test_join_team_success(self, jwt_client, user):
        admin2 = User.objects.create_user(
            email="admin2@example.com",
            password="password123",
            first_name="Admin",
            last_name="Two"
        )
        team = Team.objects.create(name="Join Team", admin=admin2)

        url = '/api/teams/join/'
        data = {"invite_code": team.invite_code}
        response = jwt_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.team == team

    def test_join_team_invalid_code(self, jwt_client):
        url = '/api/teams/join/'
        data = {"invite_code": "wrongcode"}
        response = jwt_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Неверный код приглашения" in str(response.data)
