from django.conf import settings
from django.db import models

from teams.models import Team
from users.models import User


class Task(models.Model):
    class Status(models.TextChoices):
        TO_DO = 'to_do', 'Запланирована'
        IN_PROGRESS = 'in_progress', 'В процессе'
        DONE = 'done', 'Готова'

    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    status = models.CharField(
        choices=Status.choices,
        default=Status.TO_DO,
        max_length=20,
        verbose_name='Статус задачи')

    deadline = models.DateTimeField(verbose_name='Срок исполнения')

    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='tasks_assigned',
        verbose_name='Исполнитель'
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Команда'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks_created',
        verbose_name='Создатель'
    )

    def __str__(self):
        return f'{self.title} ({self.get_status_display()})'


class TaskComment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Задача'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    content = models.TextField(
        verbose_name='Комментарий'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.author.first_name} {self.author.last_name}: ({self.content})'
