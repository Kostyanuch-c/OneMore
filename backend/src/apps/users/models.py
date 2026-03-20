import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


class Role(models.TextChoices):
    USER = 'USR', 'Пользователь'
    ADMIN = 'ADM', 'Администратор'
    TEACHER = 'TCH', 'Учитель'
    STUDENT = 'STU', 'Студент'


class User(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        verbose_name='Имя пользователя', max_length=150
    )

    role = models.CharField(
        verbose_name='Роль',
        choices=Role.choices,
        default=Role.USER,
    )

    @property
    def full_name(self) -> str:
        return self.get_full_name()

    def __str__(self) -> str:
        return self.username[: settings.MAX_STR_LENGTH]

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username'], name='uniq_user_username'
            ),
            models.UniqueConstraint(
                fields=['email'],
                condition=Q(email__isnull=False),
                name='uniq_user_email_when_present',
            ),
        ]
