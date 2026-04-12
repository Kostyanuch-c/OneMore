from pathlib import Path

from django.utils import timezone

import pytest

from apps.a12n.services import AuthService
from apps.users.entities import UserEntity


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
