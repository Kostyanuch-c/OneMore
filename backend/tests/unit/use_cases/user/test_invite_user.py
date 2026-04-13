from contextlib import nullcontext

from apps.users.entities import UserEntity
from apps.users.use_cases.create_user import InviteUser


def test_use_case_invite_user_called_services(
    mocker,
    user_service,
    tutor_student_membership_service,
    auth_email_service,
    user_factory,
    user_entity,
):
    get_user_by_email_mock = mocker.patch.object(
        user_service,
        'get_user_by_email',
        return_value=None,
    )

    mocker.patch.object(
        InviteUser,
        'get_username',
        return_value=user_entity.username,
    )

    membership_create_mock = mocker.patch.object(
        tutor_student_membership_service,
        'create',
        return_value=object(),
    )

    create_user_mock = mocker.patch.object(
        user_service,
        'create_user',
        return_value=user_entity,
    )

    send_invite_link_mock = mocker.patch.object(
        auth_email_service,
        'send_invite_link',
        return_value=None,
    )

    mocker.patch(
        'django.db.transaction.on_commit',
        side_effect=lambda func, robust: func(),  # noqa: ARG005
    )

    mocker.patch('django.db.transaction.atomic', return_value=nullcontext())
    tutor = user_factory.build(username='tutor')

    result = InviteUser(
        user_service=user_service,
        code_service=auth_email_service,
        tutor_user_membership_service=tutor_student_membership_service,
        student_email=user_entity.email,
        tutor_email=tutor.email,
        tutor_id=tutor.id,
    )()
    assert isinstance(result, tuple)
    new_user, is_created = result

    assert is_created is True
    assert isinstance(new_user, UserEntity)
    assert new_user.email == user_entity.email

    get_user_by_email_mock.assert_called_once_with(
        email=user_entity.email, include_inactive=True
    )

    create_user_mock.assert_called_once_with(
        username=user_entity.username,
        email=user_entity.email,
    )

    membership_create_mock.assert_called_once_with(
        student_id=user_entity.id,
        tutor_id=tutor.id,
    )

    send_invite_link_mock.assert_called_once_with(email=user_entity.email)


# TODO Дописать тесты на InviteUser
#  get_user_by_email вернул существующего пользователя;
#   create_user упал;
#    membership_service.create упал;
#       validate_not_inviting_self
