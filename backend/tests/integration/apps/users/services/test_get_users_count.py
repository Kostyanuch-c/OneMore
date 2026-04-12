from datetime import timedelta

from django.utils import timezone

import pytest

from apps.users.dto import UserFilters


@pytest.mark.parametrize(
    ('filters', 'expected_count'),
    [
        (UserFilters(), 5),
        (UserFilters(is_active=True), 2),
        (UserFilters(is_active=False), 3),
    ],
)
def test_service_get_users_count_with_various_filters(
    user_service, user_factory, filters, expected_count
):
    user_factory.create_batch(2, is_active=True)
    user_factory.create_batch(3, is_active=False)

    assert user_service.get_users_count(filters) == expected_count


def test_service_get_user_count_with_search_filter(user_service, user_factory):
    user_factory(username='alex123', email='alex@example.com')
    user_factory(username='john456', email='john@example.com')

    filters = UserFilters(search='alex')

    assert user_service.get_users_count(filters) == 1


def test_service_get_user_count_not_found(user_service, user_factory):
    user_factory(username='Miss', email='miss@mail.ru')

    filters = UserFilters(search='find')
    assert user_service.get_users_count(filters) == 0


def test_service_get_user_count_full_filters(user_service, user_factory):
    filters = UserFilters(
        search='john', is_active=False, created_to=timezone.now()
    )
    user_factory(username='Miss', email='miss@mail.ru')
    user_factory(
        username='John',
        email='john@mail.ru',
        is_active=False,
        date_joined=timezone.now() + timedelta(days=1),
    )
    user_factory(
        username='mobs123',
        email='john_super@mail.ru',
        is_active=False,
        date_joined=timezone.now() - timedelta(days=1),
    )

    assert user_service.get_users_count(filters) == 1
