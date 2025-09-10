import pytest

from evaluations.api.serializers import EvaluationCreateSerializer, EvaluationSerializer


@pytest.mark.django_db
class TestEvaluationSerializer:
    def test_serialization_contains_expected_fields(self, evaluation):
        serializer = EvaluationSerializer(evaluation)
        data = serializer.data

        assert set(data.keys()) == {
            "id", "task", "task_title", "user", "user_name",
            "score", "created_by", "created_by_name", "comment", "created_at"
        }
        assert data["task_title"] == evaluation.task.title
        assert data["user_name"] == evaluation.user.get_full_name()
        assert data["created_by_name"] == evaluation.created_by.get_full_name()


@pytest.mark.django_db
class TestEvaluationCreateSerializer:
    def test_valid_data_creates_evaluation(self, manager, employee, task, rf):
        request = rf.post("/api/evaluations/")
        request.user = manager
        task.status = task.Status.DONE
        task.save()

        serializer = EvaluationCreateSerializer(
            data={
                "task": task.id,
                "user": employee.id,
                "score": 5,
                "comment": "Отлично"
            },
            context={"request": request}
        )
        assert serializer.is_valid(), serializer.errors
        evaluation = serializer.save()
        assert evaluation.created_by == manager
        assert evaluation.task == task
        assert evaluation.user == employee
        assert evaluation.score == 5

    def test_invalid_if_task_not_done(self, manager, employee, task, rf):
        task.status = task.Status.IN_PROGRESS
        task.save()

        request = rf.post("/api/evaluations/")
        request.user = manager

        serializer = EvaluationCreateSerializer(
            data={
                "task": task.id,
                "user": employee.id,
                "score": 4,
                "comment": "Еще не доделал"
            },
            context={"request": request}
        )
        assert not serializer.is_valid()
        assert "Оценка может быть выставлена только выполненной задаче." in str(
            serializer.errors)

    def test_invalid_if_duplicate(
            self,
            evaluation,
            manager,
            employee,
            task,
            rf):
        request = rf.post("/api/evaluations/")
        request.user = manager
        task.status = task.Status.DONE
        task.save()

        serializer = EvaluationCreateSerializer(
            data={
                "task": task.id,
                "user": employee.id,
                "score": 5,
                "comment": "Повтор"
            },
            context={"request": request}
        )
        assert not serializer.is_valid()
        assert "Вы уже оценили этого пользователя за эту задачу." in str(
            serializer.errors)
