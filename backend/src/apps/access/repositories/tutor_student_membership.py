from django.db.models import Q

from apps.access.entities import TutorStudentMembershipEntity
from apps.access.models import TutorStudentMembership
from apps.access.repositories.converter import TutorStudentMembershipConverter


class TutorStudentMembershipRepository:
    converter = TutorStudentMembershipConverter
    model = TutorStudentMembership

    def has_active_membership(self, query: Q | None = None) -> bool:
        condition = Q(is_active=True)
        if query is not None:
            condition &= query
        return self.model.objects.filter(condition).exists()

    def create(
        self,
        student_id: int,
        tutor_id: int,
    ) -> TutorStudentMembershipEntity:
        return self.converter.to_entity(
            self.model.objects.create(
                student_id=student_id,
                tutor_id=tutor_id,
            )
        )
