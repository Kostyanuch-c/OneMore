from datetime import timedelta
from pathlib import Path

from django.contrib.auth import get_user_model
from django.utils import timezone

import pytest

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
def repository():
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
def payload_create():
    return {
        'email': f'{TEST_USER_PREFIX}@example.com',
        'username': f'{TEST_USER_PREFIX}_username',
    }


@pytest.fixture
def payload_update():
    return {
        'username': f'{TEST_USER_PREFIX}_updated_username',
        'first_name': 'Updated',
        'last_name': 'User_updated',
    }
