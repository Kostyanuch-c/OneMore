import logging
import uuid
from collections.abc import Callable
from dataclasses import dataclass

from django.db import transaction

from apps.a12n.services import AuthEmailService
from apps.access.exceptions import TutorSelfInviteError
from apps.access.services import TutorStudentMembershipService
from apps.common import BaseUseCase
from apps.users.entities import UserEntity
from apps.users.services import UserService


logger = logging.getLogger('apps.users.invite')


@dataclass
class InviteUser(BaseUseCase[tuple[UserEntity, bool]]):
    user_service: UserService
    tutor_user_membership_service: TutorStudentMembershipService
    code_service: AuthEmailService
    student_email: str
    tutor_email: str
    tutor_id: int

    def act(self) -> tuple[UserEntity, bool]:
        if (user := self.get_existing_user()) is not None:
            logger.info(
                'Invite skipped: user already exists | tutor_id=%s student_id=%s field=email',
                self.tutor_id,
                user.id,
            )
            return user, False

        with transaction.atomic():
            user = self.user_service.create_user(
                username=self.get_username(), email=self.student_email
            )
            self.tutor_user_membership_service.create(
                tutor_id=self.tutor_id, student_id=user.id
            )

            logger.info(
                'User and membership created | tutor_id=%s student_id=%s field=email',
                self.tutor_id,
                user.id,
            )

            transaction.on_commit(
                func=self.send_invite,
                robust=True,
            )

            logger.info(
                'Invite callback registered | tutor_id=%s student_id=%s field=email',
                self.tutor_id,
                user.id,
            )

            return user, True

    def send_invite(self) -> None:
        # Оборачиваем в именованную функцию вместо partial для совместимости
        # с captureOnCommitCallbacks(execute=True) в версиях Django с багом #36487.
        self.code_service.send_invite_link(email=self.student_email)

    def get_username(self) -> str:
        return f'{self.student_email.split("@", 1)[0][:50]}_{uuid.uuid4().hex[:12]}'

    def get_existing_user(self) -> UserEntity | None:
        return self.user_service.get_user_by_email(
            email=self.student_email, include_inactive=True
        )

    def get_validators(self) -> list[Callable[[], None]]:
        return [self.validate_not_inviting_self]

    def validate_not_inviting_self(self) -> None:
        if self.tutor_email == self.student_email:
            logger.warning(
                'Tutor attempted to invite self | tutor_id=%s field=email',
                self.tutor_id,
            )
            raise TutorSelfInviteError
