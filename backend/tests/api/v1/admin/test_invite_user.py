import json
from http import HTTPStatus

from tests.api.utils import (
    assert_api_failure_response,
    assert_api_success_response,
    assert_api_unauthorized_response,
    get_api_data,
)

from api.schemas import MessageSchema


def test_admin_user_invite_success(
    tutor_client,
    tutor,
    admin_user_invite_url: str,
    email_for_create_user: str,
    mailoutbox,
    django_capture_on_commit_callbacks,
    django_user_model,
    membership_model,
) -> None:
    users_before = django_user_model.objects.count()
    memberships_before = membership_model.objects.count()

    with django_capture_on_commit_callbacks(execute=True) as callbacks:
        response = tutor_client.post(
            admin_user_invite_url,
            data=json.dumps({'email': email_for_create_user}),
            content_type='application/json',
        )

    assert_api_success_response(
        response=response,
        expected_status=HTTPStatus.OK,
    )
    data = get_api_data(response=response, schema=MessageSchema)
    assert data.message == 'Invite sent'

    assert django_user_model.objects.count() == users_before + 1
    assert membership_model.objects.count() == memberships_before + 1

    assert django_user_model.objects.filter(
        email=email_for_create_user
    ).exists()
    assert membership_model.objects.filter(
        student__email=email_for_create_user, tutor__email=tutor.email
    ).exists()

    assert len(callbacks) == 1
    assert len(mailoutbox) == 1


def test_admin_user_invite_existing_user_returns_ok_without_email(
    tutor_client,
    admin_user_invite_url: str,
    student,
    mailoutbox,
    django_capture_on_commit_callbacks,
    django_user_model,
    membership_model,
) -> None:
    users_before = django_user_model.objects.count()
    memberships_before = membership_model.objects.count()

    with django_capture_on_commit_callbacks(execute=True) as callbacks:
        response = tutor_client.post(
            admin_user_invite_url,
            data=json.dumps({'email': student.email}),
            content_type='application/json',
        )

    assert_api_success_response(
        response=response,
        expected_status=HTTPStatus.OK,
    )
    data = get_api_data(response=response, schema=MessageSchema)
    assert data.message == 'Invite sent'

    assert django_user_model.objects.count() == users_before
    assert membership_model.objects.count() == memberships_before + 1

    assert len(callbacks) == 0
    assert len(mailoutbox) == 0


def test_admin_user_invite_invalid_email(
    tutor_client,
    admin_user_invite_url: str,
    mailoutbox,
    django_user_model,
    membership_model,
) -> None:
    users_before = django_user_model.objects.count()
    memberships_before = membership_model.objects.count()

    response = tutor_client.post(
        admin_user_invite_url,
        data=json.dumps({'email': 'invalid_email'}),
        content_type='application/json',
    )

    assert_api_failure_response(response, HTTPStatus.UNPROCESSABLE_CONTENT)

    assert django_user_model.objects.count() == users_before
    assert membership_model.objects.count() == memberships_before
    assert len(mailoutbox) == 0


def test_admin_user_invite_unauthorized(
    client,
    admin_user_invite_url: str,
    email_for_create_user: str,
    mailoutbox,
    django_user_model,
    membership_model,
) -> None:
    users_before = django_user_model.objects.count()
    memberships_before = membership_model.objects.count()

    response = client.post(
        admin_user_invite_url,
        data=json.dumps({'email': email_for_create_user}),
        content_type='application/json',
    )
    # TODO: update response status code to 403
    assert_api_unauthorized_response(response=response)

    assert django_user_model.objects.count() == users_before
    assert membership_model.objects.count() == memberships_before
    assert len(mailoutbox) == 0
