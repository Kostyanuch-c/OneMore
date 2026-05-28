import logging
from typing import TYPE_CHECKING, Any, Protocol

from django.contrib.auth import (
    get_user_model,
    login as django_login,
    logout as django_logout,
)
from django.http import HttpRequest

from .auth_email import AuthEmailService
from apps.a12n.exceptions.email import (
    InvalidInviteTokenError,
    InvalidLoginCodeError,
)
from apps.users.entities import UserEntity
from apps.users.repositories.converter import UserConverter
from apps.users.services import UserService


if TYPE_CHECKING:
    from apps.users.models import User

logger = logging.getLogger('apps.a12n.auth')


class AuthenticationStrategy(Protocol):
    def login(self, *, request: HttpRequest, user: Any) -> None: ...

    def logout(self, *, request: HttpRequest) -> None: ...


class SessionAuthenticationStrategy(AuthenticationStrategy):
    def login(self, *, request: HttpRequest, user: User) -> None:
        django_login(request, user)

    def logout(self, *, request: HttpRequest) -> None:
        django_logout(request)


class AuthService:
    user_service = UserService()
    code_service = AuthEmailService()
    auth_strategy: AuthenticationStrategy = SessionAuthenticationStrategy()

    def _find_user_by_email(self, *, email: str) -> User | None:
        return get_user_model().objects.filter(email__iexact=email).first()

    def _get_user_model_by_email(self, *, email: str) -> User:
        user = self._find_user_by_email(email=email)
        if user is None:
            logger.error(
                'Invariant violation: invite token resolved to missing user'
            )
            raise RuntimeError('Invite token resolved to missing user')
        return user

    def request_login_code(self, *, email: str) -> None:
        if not self._find_user_by_email(email=email):
            logger.warning('Login code request rejected')
            return

        logger.info('Login code requested')
        self.code_service.send_login_code(email=email)

    def confirm(
        self,
        *,
        request: HttpRequest,
        email: str,
        code: str,
    ) -> UserEntity:
        user = self._find_user_by_email(email=email)

        if user is None or not self.code_service.verify_login_code(
            email=email, code=code
        ):
            logger.warning('Login confirmation failed')
            raise InvalidLoginCodeError

        self.auth_strategy.login(request=request, user=user)
        logger.info('User logged in successfully | user_id=%s', user.id)
        return UserConverter.to_entity(model=user)

    def invite_confirm(
        self, *, request: HttpRequest, token: str
    ) -> UserEntity:
        email = self.code_service.verify_invite_token(token=token)
        if email is None:
            logger.warning('Invalid invite token')
            raise InvalidInviteTokenError

        user = self._get_user_model_by_email(email=email)

        self.auth_strategy.login(request=request, user=user)
        return UserConverter.to_entity(model=user)

    def logout(self, *, request: HttpRequest) -> None:
        self.auth_strategy.logout(request=request)
        logger.info('User logged out')
