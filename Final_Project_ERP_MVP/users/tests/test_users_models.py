import pytest
from django.db import IntegrityError

from teams.models import Team
from users.models import User


@pytest.mark.django_db
class TestUserModel:
    def test_create_user_with_email(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="strongpassword123",
            first_name="Иван",
            last_name="Иванов"
        )
        assert user.email == "test@example.com"
        assert user.check_password("strongpassword123")
        assert user.role == User.Role.USER

    def test_unique_email_constraint(self):
        User.objects.create_user(
            email="duplicate@example.com",
            password="password"
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email="duplicate@example.com",
                password="password2"
            )

    def test_default_role_is_user(self):
        user = User.objects.create_user(
            email="rolecheck@example.com",
            password="password"
        )
        assert user.role == User.Role.USER

    def test_str_method(self):
        user = User.objects.create_user(
            email="strtest@example.com",
            password="password",
            first_name="Анна",
            last_name="Смирнова",
            role=User.Role.MANAGER
        )
        assert str(user) == "Анна Смирнова (manager)"

    def test_user_can_be_assigned_to_team(self, django_db_blocker):
        with django_db_blocker.unblock():
            admin = User.objects.create_user(
                email="admin@example.com",
                password="password",
                first_name="Admin",
                last_name="Adminov",
                role=User.Role.ADMIN_TEAM
            )
            team = Team.objects.create(name="Test Team", admin=admin)
            user = User.objects.create_user(
                email="teamuser@example.com",
                password="password",
                team=team
            )

            assert user.team == team
            assert user in team.members.all()
