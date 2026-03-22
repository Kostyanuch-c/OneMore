from dataclasses import dataclass

from apps.common import BaseEntity


@dataclass
class TutorStudentMembershipEntity(BaseEntity):
    tutor_id: int
    student_id: int
    is_active: bool = True

    def deactivate(self) -> None:
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True
