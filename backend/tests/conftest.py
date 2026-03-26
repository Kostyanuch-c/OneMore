from django.test import Client

import pytest

from tests.factories.tutor_student_membership import (
    TutorStudentMembershipFactory,
)
from tests.factories.user import UserFactory

from apps.access.services import TutorStudentMembershipService
from apps.users.services import UserService


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
def tutor_student_membership_service():
    return TutorStudentMembershipService()
