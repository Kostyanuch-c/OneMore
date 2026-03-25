from datetime import datetime

from apps.users.entities import UserEntity


def _assert_common_user_fields(
    user, email, username, is_active, is_staff, first_name='', last_name=''
) -> None:
    assert user.email == email
    assert user.username == username
    assert user.is_active is is_active
    assert user.is_staff is is_staff
    assert user.date_joined is not None
    assert isinstance(user.date_joined, datetime)
    assert user.first_name == first_name
    assert user.last_name == last_name


def assert_user_entity(
    user: UserEntity,
    *,
    email: str,
    username: str,
    user_id: int | None = None,
    is_active: bool = True,
    is_staff: bool = False,
    first_name: str = '',
    last_name: str = '',
) -> None:
    assert isinstance(user, UserEntity)
    if user_id is not None:
        assert user.id == user_id
    _assert_common_user_fields(
        user, email, username, is_active, is_staff, first_name, last_name
    )


def assert_user_model(
    user,
    *,
    email: str,
    username: str,
    is_active: bool = True,
    is_staff: bool = False,
    has_usable_password: bool = False,
    first_name: str = '',
    last_name: str = '',
) -> None:
    _assert_common_user_fields(
        user, email, username, is_active, is_staff, first_name, last_name
    )
    assert user.has_usable_password() is has_usable_password


def serialize_users_for_snapshot(user_model):
    return list(
        user_model.objects.order_by('id').values(
            'id',
            'email',
            'username',
            'is_active',
            'is_staff',
            'date_joined',
            'password',
        )
    )
