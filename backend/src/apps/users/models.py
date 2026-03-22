import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(
        'UUID',
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    email = models.EmailField(
        'Email',
        unique=True,
        blank=False,
    )

    is_tutor = models.BooleanField(
        'Репетитор',
        default=False,
        help_text='Может выступать репетитором в TutorStudentMembership',
    )

    @property
    def full_name(self) -> str:
        return self.get_full_name()

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username[: settings.MAX_STR_LENGTH]
