import logging
from datetime import datetime

from django.db import IntegrityError
from django.db.models import Q

from apps.access.constants import (
    TUTOR_STUDENT_DIFFERENT_USERS_CONSTRAINT,
    TUTOR_STUDENT_UNIQUE_CONSTRAINT,
)
from apps.access.entities import TutorStudentMembershipEntity
from apps.access.exceptions import (
    TutorAndStudentMustBeDifferentError,
    TutorStudentAlreadyExistsError,
    TutorStudentIntegrityError,
)
from apps.access.repositories import TutorStudentMembershipRepository
from apps.common.utils import constraint_name


logger = logging.getLogger('apps.access.membership')


class TutorStudentMembershipService:
    repository = TutorStudentMembershipRepository()

    def _build_query(
        self,
        *,
        student_id: int,
        tutor_id: int | None = None,
        created_at: datetime | None = None,
    ) -> Q:
        query = Q(student_id=student_id)
        if created_at is not None:
            query &= Q(created_at__gte=created_at)
        if tutor_id is not None:
            query &= Q(tutor_id=tutor_id)
        return query

    def has_active_membership(
        self, *, student_id: int, tutor_id: int | None = None
    ) -> bool:
        return self.repository.has_active_membership(
            query=self._build_query(student_id=student_id, tutor_id=tutor_id)
        )

    def create(
        self, *, tutor_id: int, student_id: int
    ) -> TutorStudentMembershipEntity:
        try:
            return self.repository.create(
                student_id=student_id,
                tutor_id=tutor_id,
            )
        except IntegrityError as error:
            name = constraint_name(error)

            logger.warning(
                'Failed to create tutor-student membership | tutor_id=%s student_id=%s constraint=%s',
                tutor_id,
                student_id,
                name,
            )

            if name == TUTOR_STUDENT_UNIQUE_CONSTRAINT:
                raise TutorStudentAlreadyExistsError from error

            if name == TUTOR_STUDENT_DIFFERENT_USERS_CONSTRAINT:
                raise TutorAndStudentMustBeDifferentError from error

            if name and 'student_id' in name:
                raise TutorStudentIntegrityError(
                    message='Student not found',
                    extra={'field': ['student_id'], 'student_id': student_id},
                ) from error

            if name and 'tutor_id' in name:
                raise TutorStudentIntegrityError(
                    message='Tutor not found',
                    extra={'field': ['tutor_id'], 'tutor_id': tutor_id},
                ) from error

            logger.exception('Unknown integrity error')
            raise TutorStudentIntegrityError from error
