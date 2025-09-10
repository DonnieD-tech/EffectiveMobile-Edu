import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.timezone import now

from evaluations.models import Evaluation


@pytest.mark.django_db
def test_create_valid_evaluation(task, user, manager):
    evaluation = Evaluation.objects.create(
        task=task,
        user=user,
        score=4,
        created_by=manager,
        comment="Хорошая работа"
    )
    assert evaluation.pk is not None
    assert evaluation.score == 4
    assert evaluation.comment == "Хорошая работа"


@pytest.mark.django_db
def test_score_must_be_between_1_and_5(task, user, manager):
    evaluation = Evaluation(
        task=task,
        user=user,
        score=0,
        created_by=manager,
    )
    with pytest.raises(ValidationError):
        evaluation.full_clean()

    evaluation.score = 6
    with pytest.raises(ValidationError):
        evaluation.full_clean()


@pytest.mark.django_db
def test_unique_together_constraint(task, user, manager):
    Evaluation.objects.create(
        task=task,
        user=user,
        score=3,
        created_by=manager,
    )
    with pytest.raises(IntegrityError):
        Evaluation.objects.create(
            task=task,
            user=user,
            score=5,
            created_by=manager,
        )


@pytest.mark.django_db
def test_created_at_is_set(task, user, manager):
    evaluation = Evaluation.objects.create(
        task=task,
        user=user,
        score=2,
        created_by=manager,
    )
    assert evaluation.created_at is not None
    assert evaluation.created_at <= now()


@pytest.mark.django_db
def test_comment_can_be_blank(task, user, manager):
    evaluation = Evaluation.objects.create(
        task=task,
        user=user,
        score=5,
        created_by=manager,
        comment=""
    )
    assert evaluation.comment == ""
