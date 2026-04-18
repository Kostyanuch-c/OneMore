import logging
from typing import Any, Protocol

from django.contrib.auth import get_user_model, login
from django.http import HttpRequest

from .auth_email import AuthEmailService
from apps.a12n.exceptions.email import (
    InvalidInviteTokenError,
    InvalidLoginCodeError,
)
from apps.users.entities import UserEntity
from apps.users.models import User
from apps.users.repositories.converter import UserConverter
from apps.users.services import UserService


logger = logging.getLogger('apps.a12n.auth')


class LoginStrategy(Protocol):
    def login(self, request: Any, user: Any) -> Any: ...


class SessionLoginStrategy(LoginStrategy):
    def login(self, request: HttpRequest, user: User) -> None:
        login(request, user)


class AuthService:
    user_service = UserService()
    code_service = AuthEmailService()
    login_strategy: LoginStrategy = SessionLoginStrategy()

    def _find_user_by_email(self, email: str) -> User | None:
        return get_user_model().objects.filter(email__iexact=email).first()

    def _get_user_model_by_email(self, email: str) -> User:
        user = self._find_user_by_email(email=email)
        if user is None:
            logger.error(
                'Invariant violation: invite token resolved to missing user'
            )
            raise RuntimeError('Invite token resolved to missing user')
        return user

    def authorise(self, email: str) -> None:
        if not self._find_user_by_email(email):
            logger.warning('Login code request rejected')
            return

        logger.info('Login code requested')
        self.code_service.send_login_code(email)

    def confirm(
        self,
        request: HttpRequest,
        email: str,
        code: str,
    ) -> UserEntity:
        user = self._find_user_by_email(email)

        if user is None or not self.code_service.verify_login_code(
            email, code
        ):
            logger.warning(
                'Login confirmation failed',
            )
            raise InvalidLoginCodeError

        self.login_strategy.login(request, user)
        logger.info('User logged in successfully | user_id=%s', user.id)
        return UserConverter.to_entity(user)

    def invite_confirm(self, request: HttpRequest, token: str) -> UserEntity:
        email = self.code_service.verify_invite_token(token)
        if email is None:
            logger.warning('Invalid invite token')
            raise InvalidInviteTokenError

        user = self._get_user_model_by_email(email=email)

        self.login_strategy.login(request, user)
        return UserConverter.to_entity(user)
