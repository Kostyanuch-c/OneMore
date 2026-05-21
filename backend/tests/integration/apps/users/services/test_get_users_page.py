from datetime import timedelta

from django.utils import timezone

import pytest

from apps.users.dto import UserFilters
from apps.users.entities import UserEntity


@pytest.mark.parametrize(
    ('filters', 'expected_total'),
    [
        (UserFilters(), 5),
        (UserFilters(is_active=True), 2),
        (UserFilters(is_active=False), 3),
    ],
)
def test_get_users_page_returns_total_with_various_filters(
    user_service,
    user_factory,
    filters,
    expected_total,
):
    user_factory.create_batch(2, is_active=True)
    user_factory.create_batch(3, is_active=False)

    page = user_service.get_users_page(
        filters=filters,
        limit=10,
        offset=0,
    )

    assert page.total == expected_total
    assert len(page.items) == expected_total
    assert all(isinstance(user, UserEntity) for user in page.items)


@pytest.mark.parametrize(
    ('is_active', 'limit', 'offset', 'expected_items_count', 'expected_total'),
    [
        (None, 15, 0, 15, 15),
        (None, 4, 0, 4, 15),
        (None, 5, 5, 5, 15),
        (False, 15, 0, 10, 10),
        (True, 5, 0, 5, 5),
    ],
)
def test_get_users_page_returns_expected_users(
    user_service,
    users,
    user_model,
    is_active,
    limit,
    offset,
    expected_items_count,
    expected_total,
):
    filters = UserFilters(is_active=is_active)

    expected_source = users
    if is_active is not None:
        expected_source = [
            user for user in users if user.is_active is is_active
        ]

    expected_users = expected_source[offset : offset + limit]

    page = user_service.get_users_page(
        filters=filters,
        limit=limit,
        offset=offset,
    )

    assert page.total == expected_total
    assert len(page.items) == expected_items_count
    assert all(isinstance(user, UserEntity) for user in page.items)
    assert [user.id for user in page.items] == [
        user.id for user in expected_users
    ]
    assert user_model.objects.count() == len(users)


def test_get_users_page_filters_by_search(user_service, user_factory):
    expected_user = user_factory(username='alex123', email='alex@example.com')
    user_factory(username='john456', email='john@example.com')

    page = user_service.get_users_page(
        filters=UserFilters(search='alex'),
        limit=10,
        offset=0,
    )

    assert page.total == 1
    assert len(page.items) == 1
    assert page.items[0].id == expected_user.id


def test_get_users_page_returns_empty_page_when_no_users_match(
    user_service,
    users,
):
    page = user_service.get_users_page(
        filters=UserFilters(search='missing@example.com', is_active=False),
        limit=10,
        offset=0,
    )

    assert page.total == 0
    assert page.items == []


def test_get_users_page_filters_by_full_filters(
    user_service,
    user_factory,
):
    now = timezone.now()

    user_factory(username='Miss', email='miss@mail.ru')
    user_factory(
        username='John',
        email='john@mail.ru',
        is_active=False,
        date_joined=now + timedelta(days=1),
    )
    expected_user = user_factory(
        username='mobs123',
        email='john_super@mail.ru',
        is_active=False,
        date_joined=now - timedelta(days=1),
    )

    filters = UserFilters(
        search='john',
        is_active=False,
        created_to=now,
    )

    page = user_service.get_users_page(
        filters=filters,
        limit=10,
        offset=0,
    )

    assert page.total == 1
    assert len(page.items) == 1
    assert page.items[0].id == expected_user.id
