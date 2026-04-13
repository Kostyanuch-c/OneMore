from django.core.cache import cache
from django.test import Client

import pytest

from tests.factories.tutor_student_membership import (
    TutorStudentMembershipFactory,
)
from tests.factories.user import UserFactory

from apps.a12n.services import AuthEmailService
from apps.access.services import TutorStudentMembershipService
from apps.users.services import UserService
from apps.users.use_cases.create_user import InviteUser


@pytest.fixture(autouse=True)
def clear_django_cache():
    cache.clear()


@pytest.fixture
def nonexistent_id():
    return 10**12


@pytest.fixture
def api_client():
    """Фикстура для Django Ninja клиента."""
    return Client()


@pytest.fixture
def user(db):
    """Фикстура для создания пользователя через фабрику."""
    return UserFactory()


@pytest.fixture
def auth_client(api_client, user):
    """Фикстура для аутентифицированного клиента."""
    api_client.force_login(user)
    return api_client


@pytest.fixture
def user_factory():
    """Фикстура для создания пользователей через фабрику."""
    return UserFactory


@pytest.fixture
def user_service():
    return UserService()


@pytest.fixture
def tutor_student_membership_factory():
    return TutorStudentMembershipFactory


@pytest.fixture
def membership(tutor_student_membership_factory):
    return tutor_student_membership_factory()


@pytest.fixture
def tutor_student_membership_service() -> TutorStudentMembershipService:
    return TutorStudentMembershipService()


@pytest.fixture
def auth_email_service() -> AuthEmailService:
    return AuthEmailService()


@pytest.fixture
def use_case_invite_user(
    tutor_student_membership_service,
    user_service,
    auth_email_service,
    user_factory,
) -> InviteUser:
    tutor = user_factory.create(username='tutor', email='tutor@mail.ru')
    return InviteUser(
        user_service=user_service,
        code_service=auth_email_service,
        tutor_user_membership_service=tutor_student_membership_service,
        student_email='new_student_123@mail.com',
        tutor_email=tutor.email,
        tutor_id=tutor.id,
    )
