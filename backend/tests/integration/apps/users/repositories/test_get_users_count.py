from django.core.exceptions import FieldError
from django.db.models import Q

import pytest


def test_get_users_count_without_filters(repository, user, user_model):
    assert repository.get_users_count() == user_model.objects.count()


def test_get_users_count_with_filters(repository, user, user_model):
    filters = Q(is_active=False)

    assert (
        repository.get_users_count(filters)
        == user_model.objects.filter(filters).count()
    )


def test_get_users_count_returns_only_matching_users(repository, user_factory):
    user_factory.create_batch(2, is_active=True)
    user_factory.create_batch(3, is_active=False)

    assert repository.get_users_count(Q(is_active=True)) == 2  # noqa


def test_get_users_count_raises_field_error_for_unknown_filter(repository):
    with pytest.raises(FieldError):
        repository.get_users_count(Q(unknown_field=True))
