import pytest

from tasks.models import Task, TaskComment


@pytest.mark.django_db
class TestTaskModel:
    def test_create_task(self, task_factory):
        task = task_factory()
        assert Task.objects.exists()
        assert task.title == "Test Task"
        assert task.status == Task.Status.TO_DO
        assert task.team is not None
        assert task.created_by is not None

    def test_str_method(self, task_factory):
        task = task_factory(status=Task.Status.IN_PROGRESS)
        assert str(task) == f"{task.title} ({task.get_status_display()})"

    def test_status_choices(self, task_factory):
        task = task_factory(status=Task.Status.DONE)
        assert task.status in [choice[0] for choice in Task.Status.choices]
        assert task.get_status_display() == "Готова"


@pytest.mark.django_db
class TestTaskCommentModel:
    def test_create_comment(self, comment_factory):
        comment = comment_factory()
        assert TaskComment.objects.exists()
        assert comment.content == "Test comment"
        assert comment.task is not None
        assert comment.author is not None
        assert comment.created_at is not None

    def test_str_method(self, comment_factory, user_factory):
        user = user_factory(first_name="John", last_name="Doe")
        user.__class__.name = f"{user.first_name} {user.last_name}"
        comment = comment_factory(author=user, content="Sample comment")
        assert str(comment) == "John Doe: (Sample comment)"

    def test_comment_ordering(self, comment_factory):
        comment1 = comment_factory(content="First")
        comment2 = comment_factory(content="Second")
        comments = list(TaskComment.objects.all())
        assert comments[0] == comment1
        assert comments[1] == comment2
