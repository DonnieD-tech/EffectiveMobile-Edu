import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


@pytest.mark.django_db
class TestUserAPI:
    def test_register_user(self):
        url = reverse("user_register")
        data = {
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "securepass"
        }
        client = APIClient()
        response = client.post(url, data, format="json")
        assert response.status_code == 201
        assert User.objects.filter(email=data["email"]).exists()

    def test_current_user(self, jwt_client, user):
        url = reverse("user_me")
        response = jwt_client.get(url)
        assert response.status_code == 200
        assert response.data["team"] == user.team

    def test_update_current_user(self, jwt_client, user):
        url = reverse("user_me")
        data = {"first_name": "Updated"}
        response = jwt_client.patch(url, data, format="json")
        user.refresh_from_db()
        assert response.status_code == 200
        assert user.first_name == "Updated"

    def test_user_list_permissions(self, jwt_client, user, manager):
        url = reverse("user_list")
        response = jwt_client.get(url)
        assert len(response.data) == 1
        assert response.data[0]["id"] == user.id

        client = APIClient()
        client.force_authenticate(manager)
        response = client.get(url)
        assert len(response.data) == User.objects.count()

    def test_user_detail(self, jwt_client, user):
        url = reverse("user_detail", args=[user.id])
        response = jwt_client.get(url)
        assert response.status_code == 200
        assert response.data["email"] == user.email

        data = {"first_name": "NewName"}
        response = jwt_client.patch(url, data, format="json")
        user.refresh_from_db()
        assert response.status_code == 200
        assert user.first_name == "NewName"

    def test_user_detail_permissions(
            self,
            jwt_client,
            user,
            manager,
            another_user):
        url = reverse("user_detail", args=[another_user.id])
        response = jwt_client.get(url)
        assert response.status_code == 404

        client = APIClient()
        client.force_authenticate(manager)
        response = client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == another_user.id


@pytest.mark.django_db
class TestUserAPIAuth:
    def test_jwt_obtain_and_verify(self, user):
        client = APIClient()
        url = reverse('token_obtain_pair')
        data = {
            "email": user.email,
            "password": "password123"
        }
        response = client.post(url, data)
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

        verify_url = reverse('token_verify')
        access_token = response.data['access']
        verify_response = client.post(
            verify_url,
            {"token": access_token}
        )
        assert verify_response.status_code == 200

    def test_jwt_refresh(self, user):
        client = APIClient()
        obtain_url = reverse('token_obtain_pair')
        refresh_url = reverse('token_refresh')
        data = {
            "email": user.email,
            "password": "password123"
        }
        response = client.post(obtain_url, data)
        refresh_token = response.data['refresh']
        refresh_response = client.post(
            refresh_url,
            {"refresh": refresh_token}
        )
        assert refresh_response.status_code == 200
        assert "access" in refresh_response.data


@pytest.mark.django_db
class TestUserAPIDelete:
    def test_user_delete_self(self, jwt_client, user):
        url = reverse('user_detail', kwargs={"pk": user.id})
        response = jwt_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=user.id).exists()

    def test_user_cannot_delete_other(self, jwt_client, user, manager):
        url = reverse(
            'user_detail',
            kwargs={"pk": manager.id}
        )
        response = jwt_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert User.objects.filter(id=manager.id).exists()

    def test_manager_can_delete_any(self, jwt_client, manager):
        client = APIClient()
        client.force_authenticate(user=manager)
        user_to_delete = User.objects.create_user(
            email="delete_me@example.com",
            password="password123",
            first_name="Delete",
            last_name="Me"
        )
        url = reverse(
            'user_detail',
            kwargs={"pk": user_to_delete.id}
        )
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(
            id=user_to_delete.id
        ).exists()
