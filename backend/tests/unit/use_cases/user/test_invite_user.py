import pytest

from apps.access.exceptions import (
    TutorSelfInviteError,
    TutorStudentAlreadyExistsError,
)
from apps.users.entities import UserEntity
from apps.users.exceptions.users import EmailAlreadyExistsError
from apps.users.use_cases import InviteUser


@pytest.mark.usefixtures('transaction_mock')
def test_use_case_invite_user_called_services(
    mocker,
    user_service_mock,
    membership_service_mock,
    code_service_mock,
    tutor,
    user_entity,
):
    mocker.patch.object(
        InviteUser,
        'get_username',
        return_value=user_entity.username,
    )

    user_service_mock.create_user.return_value = user_entity

    mocker.patch(
        'django.db.transaction.on_commit',
        side_effect=lambda func, robust: func(),  # noqa: ARG005
    )

    result = InviteUser(
        user_service=user_service_mock,
        code_service=code_service_mock,
        tutor_user_membership_service=membership_service_mock,
        student_email=user_entity.email,
        tutor_email=tutor.email,
        tutor_id=tutor.id,
    )()
    assert isinstance(result, tuple)
    new_user, is_created = result

    assert is_created is True
    assert isinstance(new_user, UserEntity)
    assert new_user.email == user_entity.email

    user_service_mock.get_user_by_email.assert_called_once_with(
        email=user_entity.email, include_inactive=True
    )

    user_service_mock.create_user.assert_called_once_with(
        username=user_entity.username,
        email=user_entity.email,
    )

    membership_service_mock.create.assert_called_once_with(
        student_id=user_entity.id,
        tutor_id=tutor.id,
    )

    code_service_mock.send_invite_link.assert_called_once_with(
        email=user_entity.email
    )


@pytest.mark.usefixtures('transaction_mock')
def test_use_case_invite_user_return_false_if_user_already_exists(
    user_entity,
    tutor,
    user_service_mock,
    code_service_mock,
    membership_service_mock,
):
    user_service_mock.get_user_by_email.return_value = user_entity

    result = InviteUser(
        user_service=user_service_mock,
        code_service=code_service_mock,
        tutor_user_membership_service=membership_service_mock,
        student_email=user_entity.email,
        tutor_email=tutor.email,
        tutor_id=tutor.id,
    )()

    user, is_created = result
    assert user == user_entity
    assert is_created is False
    user_service_mock.get_user_by_email.assert_called_once_with(
        email=user_entity.email, include_inactive=True
    )

    user_service_mock.create_user.assert_not_called()
    membership_service_mock.create.assert_called_once_with(
        student_id=user_entity.id,
        tutor_id=tutor.id,
    )
    code_service_mock.send_invite_link.assert_not_called()


def test_use_case_invite_user_validate_not_inviting_self(
    user_service_mock, code_service_mock, membership_service_mock
):
    similar_email = 'email@mail.com'
    with pytest.raises(TutorSelfInviteError):
        InviteUser(
            user_service=user_service_mock,
            code_service=code_service_mock,
            tutor_user_membership_service=membership_service_mock,
            student_email=similar_email,
            tutor_email=similar_email,
            tutor_id=1,
        )()

    user_service_mock.get_user_by_email.assert_not_called()
    user_service_mock.create_user.assert_not_called()
    membership_service_mock.create.assert_not_called()
    code_service_mock.send_invite_link.assert_not_called()


@pytest.mark.usefixtures('transaction_mock')
@pytest.mark.parametrize(
    (
        'raised_on_user_create',
        'raised_on_membership_create',
        'expected_exception',
    ),
    [
        (True, False, EmailAlreadyExistsError),
        (False, True, TutorStudentAlreadyExistsError),
    ],
)
def test_use_case_invite_user_raise_custom_errors_on_services_errors(
    code_service_mock,
    raised_on_user_create,
    raised_on_membership_create,
    expected_exception,
    user_service_mock,
    membership_service_mock,
    mocker,
):
    if raised_on_user_create:
        user_service_mock.create_user.side_effect = EmailAlreadyExistsError()

    if raised_on_membership_create:
        membership_service_mock.create.side_effect = (
            TutorStudentAlreadyExistsError()
        )

    with pytest.raises(expected_exception):
        InviteUser(
            user_service=user_service_mock,
            code_service=code_service_mock,
            tutor_user_membership_service=membership_service_mock,
            tutor_id=1,
            tutor_email='test@mail.ru',
            student_email='student@mail.com',
        )()

    code_service_mock.send_invite_link.assert_not_called()
