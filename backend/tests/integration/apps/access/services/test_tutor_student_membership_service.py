import pytest

from apps.access.entities import TutorStudentMembershipEntity
from apps.access.exceptions import (
    TutorStudentAlreadyExistsError,
)


def test_service_create_membership(
    tutor_student_membership_service, user_factory
):
    tutor = user_factory()
    student = user_factory()

    membership = tutor_student_membership_service.create(
        student_id=student.id, tutor_id=tutor.id
    )

    assert isinstance(membership, TutorStudentMembershipEntity)
    assert membership.student_id == student.id
    assert membership.tutor_id == tutor.id


def test_service_create_membership_raises_integrity_error_on_duplicate(
    tutor_student_membership_service, membership
):
    with pytest.raises(TutorStudentAlreadyExistsError):
        tutor_student_membership_service.create(
            student_id=membership.student.id, tutor_id=membership.tutor.id
        )


def test_service_has_active_membership_true(
    tutor_student_membership_service, membership
):
    assert (
        tutor_student_membership_service.has_active_membership(
            student_id=membership.student.id, tutor_id=membership.tutor.id
        )
        is True
    )


def test_service_has_active_membership_false(
    tutor_student_membership_service, tutor_student_membership_factory
):
    membership = tutor_student_membership_factory(is_active=False)

    assert (
        tutor_student_membership_service.has_active_membership(
            student_id=membership.student.id, tutor_id=membership.tutor.id
        )
        is False
    )


def test_service_has_active_membership_by_student_only(
    tutor_student_membership_service, membership
):
    assert (
        tutor_student_membership_service.has_active_membership(
            student_id=membership.student.id
        )
        is True
    )
