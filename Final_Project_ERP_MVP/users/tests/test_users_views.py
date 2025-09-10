import pytest
from django.urls import reverse

from teams.models import Team
from users.models import User


@pytest.mark.django_db
class TestRegisterView:
    def test_get_register_page(self, client):
        url = reverse('register')
        response = client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_post_register_user(self, client):
        url = reverse('register')
        data = {
            "email": "newuser@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "first_name": "Новый",
            "last_name": "Пользователь"
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert User.objects.filter(
            email="newuser@example.com"
        ).exists()


@pytest.mark.django_db
class TestUserDetailView:
    def test_redirect_if_not_logged_in(self, client):
        url = reverse('user_detail')
        response = client.get(url)
        assert response.status_code == 302

    def test_detail_view_for_user(self, auth_client, user):
        url = reverse('user_detail')
        response = auth_client.get(url)
        assert response.status_code == 200
        assert response.context['profile_user'] == user

    def test_evaluations_context(self, auth_client, evaluation):
        url = reverse('user_detail')
        response = auth_client.get(url)

        assert response.context['evaluation_count'] == 1
        assert response.context['avg_score'] == 5
        assert len(response.context['recent_evaluations']) == 1


@pytest.mark.django_db
class TestMyLogoutView:
    def test_logout_get(self, auth_client):
        url = reverse('logout')
        response = auth_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse('login')

    def test_logout_post(self, auth_client):
        url = reverse('logout')
        response = auth_client.post(url)
        assert response.status_code == 302
        assert response.url == reverse('login')


@pytest.mark.django_db
class TestUserProfileUpdateView:
    def test_get_profile_update_page(self, auth_client):
        url = reverse('user_profile_edit')
        response = auth_client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_post_profile_update(self, auth_client, user):
        url = reverse('user_profile_edit')
        data = {
            "first_name": "Изменённое",
            "last_name": "Имя",
            "email": user.email,
            "team_code": ""
        }
        response = auth_client.post(url, data)
        user.refresh_from_db()
        assert response.status_code == 302
        assert user.first_name == "Изменённое"

    def test_post_profile_update_with_team(self, auth_client, user, db):
        team = Team.objects.create(name="Test Team", admin=user)
        url = reverse('user_profile_edit')
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "team_code": team.invite_code
        }
        response = auth_client.post(url, data)
        user.refresh_from_db()
        assert response.status_code == 302
        assert user.team == team


@pytest.mark.django_db
class TestUserDeleteView:
    def test_get_delete_page(self, auth_client):
        url = reverse('user_delete')
        response = auth_client.get(url)
        assert response.status_code == 200
        assert "profile_user" not in response.context

    def test_post_delete_user(self, auth_client, user):
        url = reverse('user_delete')
        response = auth_client.post(url)
        assert response.status_code == 302
        assert not User.objects.filter(pk=user.pk).exists()
