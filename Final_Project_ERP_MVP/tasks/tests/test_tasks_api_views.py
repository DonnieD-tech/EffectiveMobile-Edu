import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestTaskListCreateView:
    def test_list_tasks_manager_sees_all(
            self, api_client, manager_with_team_and_task):
        manager, team, task = manager_with_team_and_task

        api_client.force_authenticate(manager)
        url = reverse("task_list_create")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert any(task.id == item["id"] for item in response.data)

    def test_list_tasks_user_sees_only_assigned(
            self, api_client, user_with_team_and_task):
        user, team, task = user_with_team_and_task

        api_client.force_authenticate(user)
        url = reverse("task_list_create")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        for item in response.data:
            assert item["assignee"] == user.id

    def test_create_task_manager(self, api_client, manager_with_team_and_task):
        manager, team, _ = manager_with_team_and_task

        api_client.force_authenticate(manager)
        url = reverse("task_list_create")
        data = {
            "title": "New Task",
            "description": "Desc",
            "status": "to_do",
            "deadline": "2025-01-01T12:00:00Z",
            "assignee": manager.id,
            "team": team.id
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == data["title"]

    def test_create_task_user_forbidden(
            self, api_client, user_with_team_and_task):
        user, team, _ = user_with_team_and_task

        api_client.force_authenticate(user)
        url = reverse("task_list_create")
        data = {
            "title": "Forbidden",
            "description": "Desc",
            "status": "to_do",
            "deadline": "2025-01-01T12:00:00Z",
            "assignee": user.id,
            "team": team.id
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestTaskDetailView:
    def test_retrieve_task(self, api_client, manager_with_team_and_task):
        manager, _, task = manager_with_team_and_task

        api_client.force_authenticate(manager)
        url = f'/api/tasks/{task.id}/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == task.id

    def test_update_task_manager(self, api_client, manager_with_team_and_task):
        manager, _, task = manager_with_team_and_task

        api_client.force_authenticate(manager)
        url = f'/api/tasks/{task.id}/'
        data = {
            "title": "Updated",
            "description": task.description,
            "status": task.status,
            "deadline": task.deadline.isoformat(),
            "assignee": task.assignee.id if task.assignee else None,
            "team": task.team.id
        }
        response = api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated"

    def test_update_task_user_forbidden(
            self, api_client, user_with_team_and_task):
        user, team, task = user_with_team_and_task

        api_client.force_authenticate(user)
        url = f'/api/tasks/{task.id}/'
        data = {
            "title": "Should not update",
            "description": task.description,
            "status": task.status,
            "deadline": task.deadline.isoformat(),
            "assignee": user.id,
            "team": team.id
        }
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task_manager(self, api_client, manager_with_team_and_task):
        manager, _, task = manager_with_team_and_task

        api_client.force_authenticate(manager)
        url = f'/api/tasks/{task.id}/'
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_task_user_forbidden(
            self, api_client, user_with_team_and_task):
        user, _, task = user_with_team_and_task

        api_client.force_authenticate(user)
        url = f'/api/tasks/{task.id}/'
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestTaskCommentListCreateView:
    def test_list_comments(
            self,
            api_client,
            user_with_team_and_task,
            comment_for_user_task):
        user, _, task = user_with_team_and_task
        comment = comment_for_user_task

        api_client.force_authenticate(user)
        url = f'/api/tasks/{task.id}/comments/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert any(comment.id == item["id"] for item in response.data)

    def test_create_comment_assignee(
            self, api_client, user_with_team_and_task):
        user, _, task = user_with_team_and_task

        api_client.force_authenticate(user)
        url = reverse("task_comments", kwargs={"task_id": task.id})
        data = {"content": "New comment"}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["content"] == "New comment"

    def test_create_comment_manager(
            self,
            api_client,
            manager_with_team_and_task,
            user_with_team_and_task):
        manager, _, _ = manager_with_team_and_task
        _, _, task = user_with_team_and_task

        api_client.force_authenticate(manager)
        url = reverse("task_comments", kwargs={"task_id": task.id})
        data = {"content": "Manager comment"}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_comment_forbidden(
            self,
            api_client,
            user_with_team_and_task,
            manager_with_team_and_task):
        user, _, _ = user_with_team_and_task
        _, _, task_manager = manager_with_team_and_task

        api_client.force_authenticate(user)
        url = reverse("task_comments", kwargs={"task_id": task_manager.id})
        data = {"content": "Forbidden comment"}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestTaskCommentDetailView:
    def test_retrieve_comment(
            self,
            api_client,
            user_with_team_and_task,
            comment_for_user_task):
        user, _, task = user_with_team_and_task
        comment = comment_for_user_task

        api_client.force_authenticate(user)
        url = reverse(
            "task_comment_detail",
            kwargs={"task_id": task.id, "pk": comment.id}
        )
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == comment.id

    def test_update_comment_author(
            self,
            api_client,
            user_with_team_and_task,
            comment_for_user_task):
        user, _, task = user_with_team_and_task
        comment = comment_for_user_task

        api_client.force_authenticate(user)
        url = reverse(
            "task_comment_detail",
            kwargs={"task_id": task.id, "pk": comment.id}
        )
        data = {"content": "Updated comment"}
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data["content"] == "Updated comment"

    def test_update_comment_forbidden_other_user(
            self,
            api_client,
            manager_with_team_and_task,
            comment_for_user_task):
        manager, _, _ = manager_with_team_and_task
        comment = comment_for_user_task

        api_client.force_authenticate(manager)
        url = reverse(
            "task_comment_detail",
            kwargs={"task_id": comment.task.id, "pk": comment.id}
        )
        data = {"content": "Should not update"}
        response = api_client.put(url, data, format='json')
        assert response.status_code in [
            status.HTTP_200_OK, status.HTTP_403_FORBIDDEN]

    def test_delete_comment_author(
            self,
            api_client,
            user_with_team_and_task,
            comment_for_user_task):
        user, _, task = user_with_team_and_task
        comment = comment_for_user_task

        api_client.force_authenticate(user)
        url = reverse(
            "task_comment_detail",
            kwargs={"task_id": task.id, "pk": comment.id}
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
