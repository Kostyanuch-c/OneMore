from django.conf import settings
from django.db import models
from django.db.models import F, Q

from apps.access.constants import (
    TUTOR_STUDENT_DIFFERENT_USERS_CONSTRAINT,
    TUTOR_STUDENT_UNIQUE_CONSTRAINT,
)
from apps.common.models import BaseTimedModel


class TutorStudentMembership(BaseTimedModel):
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_memberships',
        verbose_name='Репетитор',
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tutor_memberships',
        verbose_name='Ученик',
    )

    is_active = models.BooleanField(
        'Активно',
        default=True,
    )

    class Meta:
        db_table = 'tutor_student_memberships'
        verbose_name = 'Связь репетитора и ученика'
        verbose_name_plural = 'Связи репетитора и ученика'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['tutor', 'student'],
                name=TUTOR_STUDENT_UNIQUE_CONSTRAINT,
            ),
            models.CheckConstraint(
                condition=~Q(tutor=F('student')),
                name=TUTOR_STUDENT_DIFFERENT_USERS_CONSTRAINT,
            ),
        ]
        indexes = [
            models.Index(fields=['student', 'is_active']),
        ]

    def __str__(self) -> str:
        return (
            f'{str(self.tutor)[: settings.MAX_STR_LENGTH]} -> '
            f'{str(self.student)[: settings.MAX_STR_LENGTH]}'
        )
