from django.db import IntegrityError
from django.db.models import Q

import pytest

from apps.access.exceptions import TutorStudentIntegrityError


def test_service_create_calls_repository(
    mocker, tutor_student_membership_service
):
    student_id, tutor_id = 1, 2
    expected_membership = object()

    mock_repository = mocker.patch.object(
        tutor_student_membership_service.repository,
        'create',
        return_value=expected_membership,
    )

    result = tutor_student_membership_service.create(
        tutor_id=tutor_id, student_id=student_id
    )

    mock_repository.assert_called_once_with(
        student_id=student_id, tutor_id=tutor_id
    )
    assert result is expected_membership


def test_service_create_raises_custom_error_on_integrity_error(
    mocker, tutor_student_membership_service
):
    mocker.patch.object(
        tutor_student_membership_service.repository,
        'create',
        side_effect=IntegrityError,
    )

    with pytest.raises(TutorStudentIntegrityError):
        tutor_student_membership_service.create(tutor_id=1, student_id=2)


def test_service_has_active_membership_calls_repository_with_correct_query(
    mocker, tutor_student_membership_service
):
    student_id, tutor_id = 1, 2
    built_query = Q(student_id=student_id) & Q(tutor_id=tutor_id)

    build_query_mock = mocker.patch.object(
        tutor_student_membership_service,
        '_build_query',
        return_value=built_query,
    )
    mock_repository = mocker.patch.object(
        tutor_student_membership_service.repository,
        'has_active_membership',
        return_value=True,
    )

    result = tutor_student_membership_service.has_active_membership(
        student_id=student_id, tutor_id=tutor_id
    )

    build_query_mock.assert_called_once_with(
        student_id=student_id, tutor_id=tutor_id
    )
    mock_repository.assert_called_once_with(built_query)
    assert result is True
