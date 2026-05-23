from contextlib import nullcontext
from dataclasses import asdict
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
        is_tutor=False,
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


@pytest.fixture
def login_session_mock(mocker, auth_service):
    return mocker.patch.object(
        auth_service.login_strategy,
        'login',
        return_value=None,
    )


@pytest.fixture
def user_entity_and_user(
    user_entity: UserEntity, user_factory
) -> tuple[UserEntity, dict[str, str]]:
    build_user_params = asdict(user_entity)
    build_user_params.pop('full_name', None)
    return user_entity, user_factory.build(**build_user_params)


@pytest.fixture
def get_user_model_by_email_mock(mocker, auth_service):
    return mocker.patch.object(
        auth_service,
        '_get_user_model_by_email',
        return_value=None,
    )


@pytest.fixture
def find_user_mock(mocker, auth_service):
    return mocker.patch.object(
        auth_service,
        '_find_user_by_email',
        return_value=None,
    )
