from django.db.models import Q

import pytest

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
    db_membership = membership_model.objects.get(pk=membership.id)

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


def exact_membership_query(membership):
    return Q(
        student_id=membership.student.id,
        tutor_id=membership.tutor.id,
    )


def missing_student_query(_membership):
    return Q(student_id=999999)


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
