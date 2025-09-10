from django.db import models

from users.models import User


class Meeting(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    start_time = models.DateTimeField(verbose_name="Начало")
    end_time = models.DateTimeField(verbose_name="Конец")
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE)
    participants = models.ManyToManyField(
        User,
        related_name='meetings',
        verbose_name="Участники"
    )

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return self.title

    def overlaps(self, other_meeting):
        return (self.start_time < other_meeting.end_time
                and self.end_time > other_meeting.start_time)
