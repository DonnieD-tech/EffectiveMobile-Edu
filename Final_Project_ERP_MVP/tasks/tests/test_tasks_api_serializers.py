import pytest

from tasks.api.serializers import (
    TaskCommentCreateSerializer,
    TaskCommentSerializer,
    TaskCreateUpdateSerializer,
    TaskSerializer,
)
from tasks.models import Task


@pytest.mark.django_db
class TestTaskCommentSerializer:
    def test_fields_and_author_full_name(self, comment_for_task):
        comment, author, task = comment_for_task
        serializer = TaskCommentSerializer(comment)
        data = serializer.data

        assert data["id"] == comment.id
        assert data["author"] == author.id
        assert data["author_full_name"] == f"{
            author.first_name} {
            author.last_name}"
        assert data["content"] == comment.content
        assert "created_at" in data

    def test_author_full_name_fallback_to_email(
            self, comment_for_task, user_factory):
        comment, _, task = comment_for_task
        anon_user = user_factory(
            first_name="",
            last_name="",
            email="anon@example.com")
        comment.author = anon_user
        comment.save()
        serializer = TaskCommentSerializer(comment)
        data = serializer.data
        assert data["author_full_name"] == anon_user.email


@pytest.mark.django_db
class TestTaskSerializer:
    def test_fields_and_nested_comments(
            self, task_with_assignee, comment_for_task):
        task, creator, assignee = task_with_assignee
        comment, _, _ = comment_for_task

        serializer = TaskSerializer(task)
        data = serializer.data

        assert data["id"] == task.id
        assert data["title"] == task.title
        assert data["description"] == task.description
        assert data["status"] == task.status
        assert data["assignee"] == assignee.id
        assert data["assignee_full_name"] == f"{
            assignee.first_name} {
            assignee.last_name}"
        assert data["team"] == task.team.id
        assert data["created_by"] == creator.id
        assert data["created_by_full_name"] == f"{
            creator.first_name} {
            creator.last_name}"
        assert isinstance(data["comments"], list)
        assert data["comments"][0]["id"] == comment.id

    def test_assignee_full_name_none_when_no_assignee(
            self, task_factory, user_factory):
        user = user_factory()
        task = task_factory(team=user.team, created_by=user, assignee=None)
        serializer = TaskSerializer(task)
        assert serializer.data["assignee_full_name"] is None


@pytest.mark.django_db
class TestTaskCreateUpdateSerializer:
    def test_create_assigns_created_by(self, user_factory):
        user = user_factory()
        data = {
            "title": "New Task",
            "description": "Some description",
            "status": Task.Status.TO_DO,
            "deadline": "2025-01-01T12:00:00Z",
            "assignee": user.id,
            "team": user.team.id
        }
        serializer = TaskCreateUpdateSerializer(
            data=data, context={
                "request": type(
                    "Req", (), {
                        "user": user})()})
        assert serializer.is_valid()
        task = serializer.save()
        assert task.created_by == user
        assert task.title == data["title"]


@pytest.mark.django_db
class TestTaskCommentCreateSerializer:
    def test_create_comment(self, user_factory, task_factory):
        user = user_factory()
        task = task_factory(team=user.team, created_by=user)
        data = {"content": "A comment"}
        serializer = TaskCommentCreateSerializer(data=data)
        assert serializer.is_valid()
        comment = serializer.save(author=user, task=task)
        assert comment.content == data["content"]
        assert comment.author == user
        assert comment.task == task
