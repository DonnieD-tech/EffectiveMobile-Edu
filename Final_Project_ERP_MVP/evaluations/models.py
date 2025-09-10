from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Evaluation(models.Model):
    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name='Задача'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='received_evaluations',
        verbose_name='Пользователь'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name='Оценка'
    )
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='given_evaluations',
        verbose_name='Создано'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        unique_together = (
            'task',
            'user',
            'created_by'
        )
