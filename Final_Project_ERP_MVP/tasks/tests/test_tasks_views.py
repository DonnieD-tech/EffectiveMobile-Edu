import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils import timezone

from tasks.models import Task
from users.models import User


@pytest.mark.django_db
class TestTaskDetailView:
    def test_access(self, client, user_factory, task_factory):
        user = user_factory(role=User.Role.MANAGER)
        client.force_login(user)
        task = task_factory(team=user.team)

        url = reverse(
            "task_detail",
            kwargs={"pk": task.id}
        )
        response = client.get(url)

        assert response.status_code == 200
        assert response.context["task"] == task

    def test_wrong_team(
            self,
            client,
            user_factory,
            task_factory,
            team_factory):
        user = user_factory()
        other_team = team_factory()
        task = task_factory(team=other_team)

        client.force_login(user)
        url = reverse(
            "task_detail",
            kwargs={"pk": task.id}
        )
        response = client.get(url)

        assert response.status_code == 404


@pytest.mark.django_db
class TestTaskCreateView:
    def test_success(self, client, user_factory):
        user = user_factory()
        client.force_login(user)

        url = reverse("task_create")
        data = {
            "title": "New Task",
            "description": "Task description",
            "assignee": user.id,
            "deadline": timezone.now() + timezone.timedelta(days=7),
            "team": user.team.id
        }
        response = client.post(url, data)

        assert response.status_code == 302
        assert Task.objects.filter(
            title="New Task",
            team=user.team
        ).exists()

    def test_no_team(self, client, user_factory):
        user = user_factory()
        user.team = None
        user.save()
        client.force_login(user)

        url = reverse("task_create")
        response = client.post(
            url,
            {"title": "Task without team"}
        )

        assert response.status_code == 200
        assert not Task.objects.filter(
            title="Task without team"
        ).exists()


@pytest.mark.django_db
class TestTaskListView:
    def test_list(self, client, user_factory, task_factory):
        user = user_factory()
        task = task_factory(team=user.team)
        client.force_login(user)

        url = reverse("task_list")
        response = client.get(url)

        assert response.status_code == 200
        assert task in response.context["tasks"]


@pytest.mark.django_db
class TestTaskUpdateView:
    def test_success(self, client, user_factory, task_factory):
        user = user_factory(role=User.Role.MANAGER)
        task = task_factory(
            team=user.team,
            deadline=timezone.now() + timezone.timedelta(days=7)
        )
        client.force_login(user)

        url = reverse(
            "task_update",
            kwargs={"pk": task.id}
        )
        data = {
            "title": "Updated Task",
            "description": task.description,
            "assignee": user.id,
            "deadline": task.deadline,
        }
        response = client.post(url, data)
        task.refresh_from_db()

        assert response.status_code == 302
        assert task.title == "Updated Task"

    def test_no_permission(self, client, user_factory, task_factory):
        user = user_factory(role=User.Role.USER)
        task = task_factory(team=user.team)
        client.force_login(user)

        url = reverse(
            "task_update",
            kwargs={"pk": task.id}
        )
        response = client.post(
            url,
            {"title": "Fail Update", "assignee": user.id}
        )
        task.refresh_from_db()

        assert response.status_code == 200
        assert task.title != "Fail Update"


@pytest.mark.django_db
class TestTaskCommentCreateView:
    def test_create_comment(self, client, user_factory, task_factory):
        user = user_factory()
        task = task_factory(team=user.team)
        client.force_login(user)

        url = reverse(
            "task_comment_create",
            kwargs={"pk": task.id}
        )
        response = client.post(
            url,
            {"content": "New comment"}
        )

        assert response.status_code == 302
        assert task.comments.filter(
            content="New comment"
        ).exists()


@pytest.mark.django_db
class TestTaskChangeStatusView:
    def test_success(self, client, user_factory, task_factory):
        user = user_factory(role=User.Role.MANAGER)
        task = task_factory(team=user.team)
        client.force_login(user)

        url = reverse(
            "task_change_status",
            kwargs={"pk": task.id}
        )
        response = client.post(
            url,
            {"status": Task.Status.DONE}
        )
        task.refresh_from_db()

        assert response.status_code == 302
        assert task.status == Task.Status.DONE

    def test_invalid_status(self, client, user_factory, task_factory):
        user = user_factory(role=User.Role.MANAGER)
        task = task_factory(team=user.team)
        client.force_login(user)

        url = reverse(
            "task_change_status",
            kwargs={"pk": task.id}
        )
        response = client.post(
            url,
            {"status": "WRONG"}
        )
        task.refresh_from_db()

        assert task.status == Task.Status.TO_DO
        messages = list(get_messages(response.wsgi_request))
        assert any("Некорректный статус" in str(m) for m in messages)

    def test_no_permission(self, client, user_factory, task_factory):
        user = user_factory(role=User.Role.USER)
        task = task_factory(team=user.team)
        client.force_login(user)

        url = reverse(
            "task_change_status",
            kwargs={"pk": task.id}
        )
        response = client.post(
            url,
            {"status": Task.Status.DONE}
        )
        assert response.status_code == 403


@pytest.mark.django_db
class TestTeamTaskListView:
    def test_list(self, client, user_factory, task_factory):
        user = user_factory()
        task = task_factory(team=user.team)
        client.force_login(user)

        url = reverse("task_list")
        response = client.get(url)

        assert response.status_code == 200
        assert task in response.context["tasks"]


@pytest.mark.django_db
class TestTaskDeleteView:
    def test_success(self, client, user_factory, task_factory):
        user = user_factory(role=User.Role.MANAGER)
        task = task_factory(team=user.team)
        client.force_login(user)

        url = reverse("task_delete", kwargs={"pk": task.id})
        response = client.get(url)

        assert response.status_code == 302
        assert not Task.objects.filter(pk=task.id).exists()

    def test_no_permission(self, client, user_factory, task_factory):
        user = user_factory(role=User.Role.USER)
        task = task_factory(team=user.team)
        client.force_login(user)

        url = reverse("task_delete", kwargs={"pk": task.id})

        response = client.get(url)
        assert response.status_code == 403

        response = client.post(url)
        assert response.status_code == 405
