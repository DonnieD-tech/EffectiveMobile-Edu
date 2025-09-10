from django import forms
from django.contrib import admin

from tasks.models import Task
from users.models import User


class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.team:
            self.fields['assignee'].queryset = (
                User.objects.filter(
                    team=self.instance.team
                )
            )
        else:
            self.fields['assignee'].queryset = (
                User.objects.none()
            )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm
    list_display = (
        'title',
        'assignee',
        'team',
        'deadline'
    )
    list_filter = ("status", "team")
    search_fields = ("title", "description")
    ordering = ("deadline",)
