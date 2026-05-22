from django.db import IntegrityError
from django.db.models import Q

import pytest

from apps.access.exceptions import TutorStudentIntegrityError


def test_service_create_calls_repository(
    membership_repository_mock, tutor_student_membership_service
):
    student_id, tutor_id = 1, 2
    expected_membership = object()

    membership_repository_mock.create.return_value = expected_membership
    tutor_student_membership_service.repository = membership_repository_mock

    result = tutor_student_membership_service.create(
        tutor_id=tutor_id, student_id=student_id
    )

    membership_repository_mock.create.assert_called_once_with(
        student_id=student_id, tutor_id=tutor_id
    )
    assert result is expected_membership


def test_service_create_raises_custom_error_on_integrity_error(
    membership_repository_mock, tutor_student_membership_service
):
    membership_repository_mock.create.side_effect = IntegrityError(
        'some error'
    )
    tutor_student_membership_service.repository = membership_repository_mock

    with pytest.raises(TutorStudentIntegrityError):
        tutor_student_membership_service.create(tutor_id=1, student_id=2)


def test_service_has_active_membership_calls_repository_with_correct_query(
    mocker, membership_repository_mock, tutor_student_membership_service
):
    student_id, tutor_id = 1, 2
    built_query = Q(student_id=student_id) & Q(tutor_id=tutor_id)

    build_query_mock = mocker.patch.object(
        tutor_student_membership_service,
        '_build_query',
        return_value=built_query,
    )
    membership_repository_mock.has_active_membership.return_value = True
    tutor_student_membership_service.repository = membership_repository_mock

    result = tutor_student_membership_service.has_active_membership(
        student_id=student_id, tutor_id=tutor_id
    )

    build_query_mock.assert_called_once_with(
        student_id=student_id, tutor_id=tutor_id
    )
    membership_repository_mock.has_active_membership.assert_called_once_with(
        query=built_query
    )
    assert result is True
