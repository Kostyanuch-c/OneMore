import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def validate_username_reserved(username: str) -> None:
    if username.lower() in settings.RESERVED_USERNAMES:
        raise ValidationError(f"Username '{username}' is reserved.")


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[
            AbstractUser.username_validator,
            validate_username_reserved,
        ],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )

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
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username[: settings.MAX_STR_LENGTH]
