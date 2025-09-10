from django import forms

from teams.models import Team
from users.models import User


class JoinTeamForm(forms.Form):
    invite_code = forms.CharField(
        max_length=12,
        label="Код приглашения",
        widget=forms.TextInput(
            attrs={'placeholder': 'Введите код'}
        )
    )


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
        labels = {
            'name': 'Название команды'
        }


class AddMemberForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Выберите пользователя"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        if obj.team:
            return (
                f"{obj.first_name} {obj.last_name}"
                f" ({obj.team.name} - {obj.get_role_display()})"
            )
        return (
            f'{obj.first_name} {obj.last_name}'
            f' ({obj.get_role_display()})'
        )
