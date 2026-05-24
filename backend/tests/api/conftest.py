from pathlib import Path

import pytest


def pytest_collection_modifyitems(config, items):
    current_dir = Path(__file__).resolve().parent

    for item in items:
        item_path = Path(str(item.fspath)).resolve()

        if current_dir in item_path.parents or item_path.parent == current_dir:
            item.add_marker(pytest.mark.api)
            item.add_marker(pytest.mark.django_db)


@pytest.fixture
def tutor(user_factory):
    return user_factory.create(
        username='tutor',
        email='tutor@mail.ru',
        is_staff=True,
        is_tutor=True,
    )


@pytest.fixture
def student(user_factory):
    return user_factory.create(
        username='student',
        email='student@mail.com',
    )


@pytest.fixture
def tutor_client(client, tutor):
    client.force_login(tutor)
    return client


@pytest.fixture
def student_client(client, student):
    client.force_login(student)
    return client


@pytest.fixture
def random_user(user_factory):
    return user_factory.create()


@pytest.fixture
def random_auth_client(client, random_user):
    client.force_login(random_user)
    return client


@pytest.fixture
def email_for_create_user() -> str:
    return 'new_user_email@gmail.com'
