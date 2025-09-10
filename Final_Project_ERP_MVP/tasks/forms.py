from django import forms

from tasks.models import Task, TaskComment
from users.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'deadline',
            'assignee'
        ]
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'deadline': 'Срок исполнения',
            'assignee': 'Исполнитель'
        }
        widgets = {
            'deadline': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['assignee'].queryset = (
                User.objects.filter(team=user.team)
            )


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('content',)
        labels = {'content': 'Комментарий'}
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'rows': 2,
                    'placeholder': 'Напишите комментарий...'
                }
            ),
        }
