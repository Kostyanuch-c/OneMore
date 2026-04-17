from contextlib import nullcontext
from pathlib import Path

from django.utils import timezone

import pytest

from apps.a12n.services import AuthEmailService, AuthService
from apps.access.repositories import TutorStudentMembershipRepository
from apps.access.services import TutorStudentMembershipService
from apps.users.entities import UserEntity
from apps.users.repositories import UserRepository
from apps.users.services import UserService


def pytest_collection_modifyitems(config, items):
    current_dir = Path(__file__).resolve().parent

    for item in items:
        item_path = Path(str(item.fspath)).resolve()
        if current_dir in item_path.parents or item_path.parent == current_dir:
            item.add_marker(pytest.mark.unit)


@pytest.fixture
def auth_service():
    return AuthService()


@pytest.fixture
def email() -> str:
    return 'Test_2321_email@yandex.ru'


@pytest.fixture
def user_entity() -> UserEntity:
    return UserEntity(
        id=1,
        username='Test_2321',
        first_name='Test',
        last_name='User',
        full_name='Test User',
        email='new_test@mail.ru',
        is_active=True,
        is_staff=False,
        date_joined=timezone.now(),
    )


@pytest.fixture
def tutor(user_factory):
    return user_factory.build(username='tutor')


@pytest.fixture
def membership_repository_mock(mocker):
    return mocker.create_autospec(
        TutorStudentMembershipRepository, instance=True
    )


@pytest.fixture
def user_repository_mock(mocker):
    return mocker.create_autospec(UserRepository, instance=True)


@pytest.fixture
def user_service_mock(mocker):
    mock = mocker.create_autospec(UserService, instance=True)
    mock.get_user_by_email.return_value = None
    return mock


@pytest.fixture
def membership_service_mock(mocker):
    mock = mocker.create_autospec(TutorStudentMembershipService, instance=True)
    mock.create.return_value = object()
    return mock


@pytest.fixture
def code_service_mock(mocker):
    mock = mocker.create_autospec(AuthEmailService, instance=True)
    mock.send_invite_link.return_value = None
    return mock


@pytest.fixture
def transaction_mock(mocker):
    return mocker.patch(
        'django.db.transaction.atomic', return_value=nullcontext()
    )
