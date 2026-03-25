from apps.users.entities import UserEntity


def assert_user_entity(
    user: UserEntity,
    *,
    email: str,
    username: str,
    user_id: int | None = None,
    is_active: bool = True,
    is_staff: bool = False,
) -> None:
    assert isinstance(user, UserEntity)
    if user_id is not None:
        assert user.id == user_id
    assert user.email == email
    assert user.username == username
    assert user.is_active is is_active
    assert user.is_staff is is_staff


def assert_user_model(
    user,
    *,
    email: str,
    username: str,
    is_active: bool = True,
    is_staff: bool = False,
    has_usable_password: bool = False,
) -> None:
    assert user.email == email
    assert user.username == username
    assert user.is_active is is_active
    assert user.is_staff is is_staff
    assert user.has_usable_password() is has_usable_password
