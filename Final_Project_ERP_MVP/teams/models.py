import uuid

from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название"
    )
    invite_code = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        editable=False,
        verbose_name="Код для приглашения"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="admin_teams",
        verbose_name="Администратор"
    )

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = uuid.uuid4().hex[:12]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.invite_code})'
