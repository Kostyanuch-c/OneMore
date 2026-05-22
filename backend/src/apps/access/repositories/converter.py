from typing import TYPE_CHECKING

from apps.access.entities import TutorStudentMembershipEntity


if TYPE_CHECKING:
    from apps.access.models import TutorStudentMembership


class TutorStudentMembershipConverter:
    @staticmethod
    def to_entity(
        *,
        model: TutorStudentMembership,
    ) -> TutorStudentMembershipEntity:
        return TutorStudentMembershipEntity(
            id=model.pk,
            student_id=model.student_id,
            tutor_id=model.tutor_id,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
