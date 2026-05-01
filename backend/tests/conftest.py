from datetime import timedelta

from django.core.cache import cache
from django.utils import timezone

import pytest

from tests.factories.tutor_student_membership import (
    TutorStudentMembershipFactory,
)
from tests.factories.user import UserFactory

from apps.a12n.services import AuthEmailService
from apps.access.models import TutorStudentMembership
from apps.access.services import TutorStudentMembershipService
from apps.users.services import UserService
from apps.users.use_cases import InviteUser


@pytest.fixture(autouse=True)
def clear_django_cache():
    cache.clear()


@pytest.fixture
def nonexistent_id():
    return 10**12


@pytest.fixture
def user_factory() -> type[UserFactory]:
    return UserFactory


@pytest.fixture
def user(user_factory):
    return user_factory.create()


@pytest.fixture
def users(user_factory):
    now = timezone.now()
    return [
        user_factory.create(
            is_active=i < 5,  # noqa
            date_joined=now - timedelta(minutes=i),
        )
        for i in range(15)
    ]


@pytest.fixture
def user_service():
    return UserService()


@pytest.fixture
def tutor_student_membership_factory() -> type[TutorStudentMembershipFactory]:
    return TutorStudentMembershipFactory


@pytest.fixture
def membership(tutor_student_membership_factory):
    return tutor_student_membership_factory.create()


@pytest.fixture
def tutor_student_membership_service() -> TutorStudentMembershipService:
    return TutorStudentMembershipService()


@pytest.fixture
def auth_email_service() -> AuthEmailService:
    return AuthEmailService()


@pytest.fixture
def membership_model():
    return TutorStudentMembership


@pytest.fixture
def tutor(user_factory):
    return user_factory.create(
        username='tutor',
        email='tutor@mail.ru',
        is_staff=True,
    )


@pytest.fixture
def use_case_invite_user(
    tutor_student_membership_service,
    user_service,
    auth_email_service,
    user_factory,
    tutor,
) -> InviteUser:
    return InviteUser(
        user_service=user_service,
        code_service=auth_email_service,
        tutor_user_membership_service=tutor_student_membership_service,
        student_email='new_student_123@mail.com',
        tutor_email=tutor.email,
        tutor_id=tutor.id,
    )
