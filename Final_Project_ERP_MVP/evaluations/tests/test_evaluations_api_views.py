import pytest
from django.urls import reverse
from rest_framework import status

from evaluations.models import Evaluation


@pytest.mark.django_db
class TestEvaluationListCreateView:
    def test_list_as_manager_sees_all(
            self,
            api_client,
            manager,
            employee,
            task,
            evaluation):
        api_client.force_authenticate(user=manager)
        url = reverse("evaluation_list_create")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == Evaluation.objects.count()

    def test_list_as_employee_sees_only_own(
            self, api_client, employee, manager, task, evaluation):
        api_client.force_authenticate(user=employee)
        url = reverse("evaluation_list_create")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert all(ev["user"] == employee.id for ev in response.data)

    def test_create_as_manager_success(
            self, api_client, manager, employee, task):
        api_client.force_authenticate(user=manager)
        task.status = task.Status.DONE
        task.save()
        url = reverse("evaluation_list_create")
        payload = {
            "task": task.id,
            "user": employee.id,
            "score": 5,
            "comment": "Отличная работа"
        }
        response = api_client.post(url, payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert Evaluation.objects.filter(user=employee, task=task).exists()

    def test_create_as_employee_forbidden(
            self, api_client, employee, task, manager):
        api_client.force_authenticate(user=employee)
        task.status = task.Status.DONE
        task.save()
        url = reverse("evaluation_list_create")
        payload = {
            "task": task.id,
            "user": employee.id,
            "score": 3,
            "comment": "Сам себе оценку ставлю"
        }
        response = api_client.post(url, payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestEvaluationByTaskView:
    def test_list_evaluations_for_task(
            self, api_client, manager, task, evaluation):
        api_client.force_authenticate(user=manager)
        url = reverse("evaluation_by_task", args=[task.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert all(ev["task"] == task.id for ev in response.data)

    def test_list_for_task_with_no_evaluations(
            self, api_client, manager, task):
        api_client.force_authenticate(user=manager)
        url = reverse("evaluation_by_task", args=[task.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []


@pytest.mark.django_db
class TestUserAverageEvaluationView:
    def test_avg_score_without_dates(
            self,
            api_client,
            manager,
            employee,
            evaluation):
        api_client.force_authenticate(user=manager)
        url = reverse("user_average_evaluation", args=[employee.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["user_id"] == employee.id
        assert response.data["average_score"] == pytest.approx(4.0)

    def test_avg_score_with_date_filters(
            self, api_client, manager, employee, evaluation):
        api_client.force_authenticate(user=manager)
        url = reverse("user_average_evaluation", args=[employee.id])
        response = api_client.get(
            url, {"start": evaluation.created_at.date().isoformat()})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["average_score"] == pytest.approx(4.0)

    def test_avg_score_for_user_without_evaluations(
            self, api_client, manager, employee):
        api_client.force_authenticate(user=manager)
        url = reverse("user_average_evaluation", args=[employee.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["average_score"] is None
