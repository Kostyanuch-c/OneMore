import uuid
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial

from django.db import transaction

from apps.a12n.services import AuthEmailService
from apps.access.exceptions import TutorSelfInviteError
from apps.access.services import TutorStudentMembershipService
from apps.common import BaseUseCase
from apps.users.entities import UserEntity
from apps.users.services import UserService


@dataclass
class InviteUser(BaseUseCase):
    user_service: UserService
    tutor_user_membership_service: TutorStudentMembershipService
    code_service: AuthEmailService
    student_email: str
    tutor_email: str
    tutor_id: int

    def act(self) -> tuple[UserEntity, bool]:
        if (user := self.get_existing_user()) is not None:
            return user, False

        with transaction.atomic():
            user = self.user_service.create_user(
                username=self.get_username(), email=self.student_email
            )
            self.tutor_user_membership_service.create(
                tutor_id=self.tutor_id, student_id=user.id
            )
            # TODO сделать тест on commit
            transaction.on_commit(
                partial(
                    self.code_service.send_invite_link,
                    email=self.student_email,
                ),
                robust=True,
            )
            return user, True

    def get_validators(self) -> list[Callable[[], None]]:
        return [self.validate_not_inviting_self]

    def validate_not_inviting_self(self) -> None:
        if self.tutor_email == self.student_email:
            raise TutorSelfInviteError

    def get_username(self) -> str:
        return f'{self.student_email.split("@", 1)[0][:50]}_{uuid.uuid4().hex[:12]}'

    def get_existing_user(self) -> UserEntity | None:
        return self.user_service.get_user_by_email(
            email=self.student_email, include_inactive=True
        )
