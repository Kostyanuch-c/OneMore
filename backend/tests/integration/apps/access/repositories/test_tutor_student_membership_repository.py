from django.db import IntegrityError

import pytest

from tests.integration.apps.access.utils import (
    exact_membership_query,
    missing_student_query,
)
from tests.integration.utils.access_helpers import (
    assert_membership_entity,
    assert_membership_matches_db_model,
    assert_membership_model,
)


def test_create_membership(
    tutor_student_membership_repository,
    user_factory,
    membership_model,
):
    tutor = user_factory()
    student = user_factory()

    membership = tutor_student_membership_repository.create(
        student_id=student.id,
        tutor_id=tutor.id,
    )
    db_membership = membership_model.objects.get(
        student_id=student.id, tutor_id=tutor.id
    )

    assert_membership_entity(
        membership,
        student_id=student.id,
        tutor_id=tutor.id,
    )
    assert_membership_model(
        db_membership,
        student_id=student.id,
        tutor_id=tutor.id,
    )
    assert_membership_matches_db_model(membership, db_membership)

    assert membership_model.objects.count() == 1


def test_create_membership_raises_integrity_error_on_unique_together_violation(
    membership,
    tutor_student_membership_repository,
):
    with pytest.raises(IntegrityError):
        tutor_student_membership_repository.create(
            student_id=membership.student.id,
            tutor_id=membership.tutor.id,
        )


def test_create_membership_raises_integrity_error_on_tutor_equals_student(
    tutor_student_membership_repository, user
):
    with pytest.raises(IntegrityError):
        tutor_student_membership_repository.create(
            student_id=user.id,
            tutor_id=user.id,
        )


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    ('student_exists', 'tutor_exists'),
    [
        (False, True),
        (True, False),
    ],
)
def test_create_membership_raises_integrity_error_when_user_not_exists(
    tutor_student_membership_repository,
    user,
    student_exists,
    tutor_exists,
    nonexistent_id,
):
    student_id = user.id if student_exists else nonexistent_id
    tutor_id = user.id if tutor_exists else nonexistent_id

    with pytest.raises(IntegrityError):
        tutor_student_membership_repository.create(
            student_id=student_id,
            tutor_id=tutor_id,
        )


@pytest.mark.parametrize(
    ('is_active', 'query_factory', 'expected'),
    [
        (True, exact_membership_query, True),
        (False, exact_membership_query, False),
        (True, missing_student_query, False),
    ],
)
def test_has_active_membership(
    tutor_student_membership_repository,
    tutor_student_membership_factory,
    is_active,
    query_factory,
    expected,
):
    membership = tutor_student_membership_factory(is_active=is_active)

    query = query_factory(membership)
    result = tutor_student_membership_repository.has_active_membership(query)

    assert result is expected
