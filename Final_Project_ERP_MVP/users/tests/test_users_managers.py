import pytest

from users.models import User


@pytest.mark.django_db
class TestUserManager:
    def test_create_user(self):
        user = User.objects.create_user(
            email='user@example.com',
            password='password123',
            first_name='Иван',
            last_name='Иванов'
        )
        assert user.email == 'user@example.com'
        assert user.check_password('password123')
        assert not user.is_staff
        assert not user.is_superuser
        assert user.role == User.Role.USER

    def test_create_user_no_email(self):
        with pytest.raises(ValueError) as excinfo:
            User.objects.create_user(email=None, password='password123')
        assert 'email' in str(excinfo.value)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123'
        )
        assert superuser.is_staff
        assert superuser.is_superuser
        assert superuser.role == 'Admin'

    def test_create_superuser_invalid_flags(self):
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='admin123',
                is_staff=False
            )
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='admin123',
                is_superuser=False
            )
