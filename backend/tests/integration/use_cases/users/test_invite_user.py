from apps.users.entities import UserEntity


def test_use_case_invite_user_when_email_sending_fails_user_and_membership_created(
    use_case_invite_user,
    django_capture_on_commit_callbacks,
    mailoutbox,
    user_model,
    membership_model,
    settings,
):

    with django_capture_on_commit_callbacks(execute=True) as callbacks:
        result = use_case_invite_user()

        assert isinstance(result, tuple)
        new_user, is_created = result
        assert is_created is True
        assert isinstance(new_user, UserEntity)
        assert user_model.objects.count() == 2  # noqa:PLR2004
        assert membership_model.objects.count() == 1

    assert len(callbacks) == 1
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == f'Добро пожаловать в {settings.SITE_NAME}!'


def test_use_case_invite_user_error_on_email_sending_and_user_created(
    use_case_invite_user,
    django_capture_on_commit_callbacks,
    user_model,
    membership_model,
    mailoutbox,
    mocker,
):
    send_invite_link_mock = mocker.patch.object(
        use_case_invite_user.code_service,
        'send_invite_link',
        side_effect=Exception('Failed to send email'),
    )

    with django_capture_on_commit_callbacks(execute=True) as callbacks:
        result = use_case_invite_user()

        assert isinstance(result, tuple)
        new_user, is_created = result
        assert is_created is True
        assert isinstance(new_user, UserEntity)
        assert user_model.objects.count() == 2  # noqa:PLR2004
        assert membership_model.objects.count() == 1

    assert len(callbacks) == 1
    assert len(mailoutbox) == 0

    send_invite_link_mock.assert_called_once_with(
        email=use_case_invite_user.student_email
    )
