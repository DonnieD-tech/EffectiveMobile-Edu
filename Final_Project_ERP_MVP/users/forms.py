from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Минимум 8 символов"
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        help_text="Введите пароль ещё раз"
    )

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name'
        ]
        labels = {
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]


class UserUpdateForm(forms.ModelForm):
    team_code = forms.CharField(
        max_length=50,
        required=False,
        help_text="Введите код команды, чтобы присоединиться",
        label='Код команды'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]
