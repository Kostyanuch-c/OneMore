from datetime import timedelta
from pathlib import Path

from django.contrib.auth import get_user_model
from django.utils import timezone

import pytest

from apps.access.models import TutorStudentMembership
from apps.access.repositories import TutorStudentMembershipRepository
from apps.users.repositories import UserRepository


TEST_USER_PREFIX = 'test_user'


def pytest_collection_modifyitems(config, items):
    current_dir = Path(__file__).resolve().parent

    for item in items:
        item_path = Path(str(item.fspath)).resolve()
        if current_dir in item_path.parents or item_path.parent == current_dir:
            item.add_marker(pytest.mark.integration)
            item.add_marker(pytest.mark.django_db)


@pytest.fixture
def repository() -> UserRepository:
    return UserRepository()


@pytest.fixture
def user_model():
    return get_user_model()


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
def payload_create_user() -> dict[str, str]:
    return {
        'email': f'{TEST_USER_PREFIX}@example.com',
        'username': f'{TEST_USER_PREFIX}_username',
    }


@pytest.fixture
def tutor_student_membership_repository() -> TutorStudentMembershipRepository:
    return TutorStudentMembershipRepository()


@pytest.fixture
def membership_model():
    return TutorStudentMembership


@pytest.fixture
def payload_create_membership(user_factory):
    return user_factory.create(), user_factory.create()


@pytest.fixture
def email() -> str:
    return 'Test_2321_email@mail.ru'
