import pytest
from django.utils import timezone

from tasks.forms import TaskCommentForm, TaskForm
from tasks.models import Task, TaskComment


@pytest.mark.django_db
class TestTaskForm:
    def test_valid_form(self, user_factory):
        user = user_factory()
        data = {
            "title": "Test Task",
            "description": "Task description",
            "deadline": timezone.now(),
            "assignee": user.id
        }
        form = TaskForm(data=data, user=user)
        assert form.is_valid()

    def test_required_fields(self, user_factory):
        user = user_factory()
        form = TaskForm(data={}, user=user)
        assert not form.is_valid()
        assert "title" in form.errors
        assert "description" in form.errors
        assert "deadline" in form.errors

    def test_assignee_queryset(self, user_factory, team_factory):
        team = team_factory()
        user = user_factory(team=team)
        other_user = user_factory()
        form = TaskForm(user=user)
        assignee_ids = list(
            form.fields['assignee'].queryset.values_list(
                'id', flat=True))
        assert user.id in assignee_ids
        assert other_user.id not in assignee_ids

    def test_deadline_widget(self, user_factory):
        user = user_factory()
        form = TaskForm(user=user)
        widget = form.fields['deadline'].widget
        assert widget.input_type == "datetime-local"


@pytest.mark.django_db
class TestTaskCommentForm:
    def test_valid_form(self, comment_factory, user_factory, task_factory):
        user = user_factory()
        task = task_factory(team=user.team)
        data = {"content": "Sample comment"}
        form = TaskCommentForm(data=data)
        assert form.is_valid()

    def test_required_content(self):
        form = TaskCommentForm(data={})
        assert not form.is_valid()
        assert "content" in form.errors

    def test_content_widget(self):
        form = TaskCommentForm()
        widget = form.fields['content'].widget
        assert widget.attrs['rows'] == 2
        assert widget.attrs['placeholder'] == "Напишите комментарий..."


@pytest.mark.django_db
class TestTaskFormRealAction:
    def test_save_creates_task(self, user_factory):
        user = user_factory()
        data = {
            "title": "Test Task",
            "description": "Task description",
            "deadline": timezone.now(),
            "assignee": user.id
        }
        form = TaskForm(data=data, user=user)
        assert form.is_valid()
        task = form.save(commit=False)
        task.team = user.team
        task.created_by = user
        task.save()

        saved_task = Task.objects.get(id=task.id)
        assert saved_task.title == data["title"]
        assert saved_task.description == data["description"]
        assert saved_task.assignee == user
        assert saved_task.team == user.team
        assert saved_task.created_by == user


@pytest.mark.django_db
class TestTaskCommentRealAction:
    def test_save_creates_comment(self, user_factory, task_factory):
        user = user_factory()
        task = task_factory(team=user.team, created_by=user)
        data = {"content": "This is a comment"}

        form = TaskCommentForm(data=data)
        assert form.is_valid()

        comment = form.save(commit=False)
        comment.author = user
        comment.task = task
        comment.save()

        saved_comment = TaskComment.objects.get(id=comment.id)
        assert saved_comment.content == data["content"]
        assert saved_comment.author == user
        assert saved_comment.task == task
        assert saved_comment.created_at is not None
