from datetime import datetime

from django.db import IntegrityError
from django.db.models import Q

from apps.access.entities import TutorStudentMembershipEntity
from apps.access.exceptions import TutorStudentIntegrityError
from apps.access.repositories import TutorStudentMembershipRepository


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

    def create(
        self, tutor_id: int, student_id: int
    ) -> TutorStudentMembershipEntity:
        try:
            return self.repository.create(
                student_id=student_id,
                tutor_id=tutor_id,
            )
        except IntegrityError as error:
            raise TutorStudentIntegrityError from error

    def has_active_membership(
        self, student_id: int, tutor_id: int | None = None
    ) -> bool:
        return self.repository.has_active_membership(
            self._build_query(student_id=student_id, tutor_id=tutor_id)
        )
