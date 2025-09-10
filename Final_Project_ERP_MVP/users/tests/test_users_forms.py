import pytest
from django.contrib.auth import authenticate

from users.forms import UserLoginForm, UserRegisterForm, UserUpdateForm


@pytest.mark.django_db
class TestUserForms:
    def test_user_register_form_valid(self):
        form_data = {
            'email': 'test@example.com',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        }
        form = UserRegisterForm(data=form_data)
        assert form.is_valid()
        user_form = form.save()

        assert user_form.email == 'test@example.com'
        assert user_form.first_name == 'Иван'
        assert user_form.last_name == 'Иванов'
        assert user_form.check_password('strongpassword123')

    def test_user_register_form_password_mismatch(self):
        form_data = {
            'email': 'test@example.com',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'password1': 'strongpassword123',
            'password2': 'wrongpassword'
        }
        form = UserRegisterForm(data=form_data)

        assert not form.is_valid()
        assert 'password2' in form.errors

    def test_user_login_form_valid(self, user):
        form_data = {
            'username': user.email,
            'password': 'password123'
        }
        form = UserLoginForm(data=form_data)
        assert form.is_valid()

        user_auth = authenticate(
            email=user.email,
            password='password123'
        )
        assert user_auth == user

    def test_user_update_form_updates_user(self, user, team):
        form_data = {
            'first_name': 'Пётр',
            'last_name': 'Сидоров',
            'email': 'new@example.com',
            'team_code': team.invite_code
        }
        form = UserUpdateForm(
            data=form_data,
            instance=user
        )
        assert form.is_valid()

        updated_user = form.save()

        assert updated_user.first_name == 'Пётр'
        assert updated_user.last_name == 'Сидоров'
        assert updated_user.email == 'new@example.com'
