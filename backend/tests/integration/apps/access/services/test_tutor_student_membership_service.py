
import pytest

from tests.integration.utils.access_helpers import (
    assert_membership_entity,
    assert_membership_matches_db_model,
    assert_membership_model,
)

from apps.access.exceptions import (
    TutorAndStudentMustBeDifferentError,
    TutorStudentAlreadyExistsError,
    TutorStudentIntegrityError,
)


def test_service_create_membership(
    tutor_student_membership_service, user_factory, membership_model
):
    tutor = user_factory.create()
    student = user_factory.create()

    membership_entity = tutor_student_membership_service.create(
        student_id=student.id, tutor_id=tutor.id
    )

    db_membership = membership_model.objects.get(
        student_id=student.id, tutor_id=tutor.id
    )
    assert membership_model.objects.count() == 1

    assert_membership_entity(
        membership_entity,
        student_id=student.id,
        tutor_id=tutor.id,
    )
    assert_membership_model(
        db_membership,
        student_id=student.id,
        tutor_id=tutor.id,
    )
    assert_membership_matches_db_model(membership_entity, db_membership)


def test_service_create_membership_raises_custom_error_on_duplicate(
    tutor_student_membership_service, membership
):
    with pytest.raises(TutorStudentAlreadyExistsError):
        tutor_student_membership_service.create(
            student_id=membership.student.id, tutor_id=membership.tutor.id
        )


def test_service_create_membership_raises_custom_error_on_student_equals_tutor(
    tutor_student_membership_service, membership
):
    with pytest.raises(TutorAndStudentMustBeDifferentError):
        tutor_student_membership_service.create(
            student_id=membership.student.id, tutor_id=membership.student.id
        )


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    ('student_exists', 'tutor_exists', 'error_message'),
    [
        (False, True, 'Student not found'),
        (True, False, 'Tutor not found'),
    ],
)
def test_service_create_membership_raises_custom_error_when_user_not_exists(
    tutor_student_membership_service,
    user,
    student_exists,
    tutor_exists,
    nonexistent_id,
    error_message,
):
    student_id = user.id if student_exists else nonexistent_id
    tutor_id = user.id if tutor_exists else nonexistent_id

    with pytest.raises(TutorStudentIntegrityError, match=error_message):
        tutor_student_membership_service.create(
            student_id=student_id, tutor_id=tutor_id
        )


# TODO add test for has_active_membership
# TODO edit test and func in code to return entity
