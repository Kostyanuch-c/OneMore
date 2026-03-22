from django.conf import settings
from django.db import models
from django.db.models import F, Q

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
        verbose_name = 'Связь репетитора и ученика'
        verbose_name_plural = 'Связи репетитора и ученика'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['tutor', 'student'],
                name='uniq_tutor_student_pair',
            ),
            models.CheckConstraint(
                condition=~Q(tutor=F('student')),
                name='tutor_and_student_must_be_different',
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
