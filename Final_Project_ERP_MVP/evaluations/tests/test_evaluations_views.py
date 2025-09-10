import pytest
from django.urls import reverse

from evaluations.models import Evaluation
from tasks.models import Task
from users.models import User


@pytest.mark.django_db
def test_redirect_if_not_logged_in(client, task, employee):
    url = reverse(
        "evaluation_add",
        kwargs={
            "task_id": task.id,
            "user_id": employee.id})
    response = client.get(url)
    assert response.status_code == 302
    assert "/login" in response.url


@pytest.mark.django_db
def test_permission_denied_for_non_manager(client, employee, task):
    client.login(email=employee.email, password="pass123")
    url = reverse(
        "evaluation_add",
        kwargs={
            "task_id": task.id,
            "user_id": employee.id})
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_page_as_manager(client, manager, employee, task):
    client.force_login(manager)
    url = reverse(
        "evaluation_add",
        kwargs={
            "task_id": task.id,
            "user_id": employee.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "task" in response.context
    assert "target_user" in response.context
    assert response.context["task"] == task
    assert response.context["target_user"] == employee


@pytest.mark.django_db
def test_create_evaluation_success(client, manager, employee, task):
    client.force_login(manager)

    url = reverse(
        "evaluation_add",
        kwargs={
            "task_id": task.id,
            "user_id": employee.id})
    data = {
        "score": 4,
        "comment": "Good job",
    }
    response = client.post(url, data)

    if response.status_code == 404:
        users_in_team = list(
            User.objects.filter(
                team=manager.team).values_list(
                'id',
                'email'))
        tasks_for_team = list(
            Task.objects.filter(
                team=manager.team).values(
                'id',
                'title'))
        pytest.fail(
            "POST вернул 404 — возможная причина: целевой пользователь не в команде менеджера или задача не привязана к команде.\n"
            f"manager.id={manager.id}, manager.team_id={getattr(manager, 'team_id', None)}\n"
            f"employee.id={employee.id}, employee.team_id={getattr(employee, 'team_id', None)}\n"
            f"users_in_team={users_in_team}\n"
            f"tasks_for_team={tasks_for_team}\n"
            f"url={url}\n"
            f"response.content={response.content[:1000]!r}"
        )

    assert response.status_code == 302, f"Ожидался редирект 302, получен {
        response.status_code}"
    assert response.url == reverse("task_detail", kwargs={"pk": task.id})

    evaluation = Evaluation.objects.get()
    assert evaluation.task == task
    assert evaluation.user == employee
    assert evaluation.created_by == manager
    assert evaluation.score == 4
    assert evaluation.comment == "Good job"
