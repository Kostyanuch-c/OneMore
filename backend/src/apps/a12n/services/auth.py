from typing import Any, Protocol

from django.contrib.auth import get_user_model, login
from django.http import HttpRequest

from .code import AuthEmailService
from apps.users.entities import UserEntity
from apps.users.repositories.converter import UserConverter
from apps.users.services import UserService


class LoginStrategy(Protocol):
    def login(self, request: Any, user: Any) -> Any: ...


class SessionLoginStrategy(LoginStrategy):
    def login(self, request: HttpRequest, user: Any) -> None:
        login(request, user)


class AuthService:
    user_service = UserService()
    code_service = AuthEmailService()
    login_strategy = SessionLoginStrategy()

    def authorise(self, email: str) -> None:
        self.code_service.send_login_code(email)

    def confirm(
        self,
        request: HttpRequest,
        email: str,
        code: str,
    ) -> UserEntity | None:
        # TODO сделать проверку code и добавить обработку ошибок , если пользователь по емайл не найден например
        self.code_service.verify_login_code(email, code)
        user = get_user_model().objects.get(email=email)

        self.login_strategy.login(request, user)
        return UserConverter.to_entity(user)
