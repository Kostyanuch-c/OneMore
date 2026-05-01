from dataclasses import dataclass

from apps.common import BaseEntity


@dataclass(frozen=True)
class TutorStudentMembershipEntity(BaseEntity):
    tutor_id: int
    student_id: int
    is_active: bool = True
