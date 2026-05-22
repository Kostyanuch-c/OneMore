from datetime import datetime

from apps.users.entities import UserEntity
from apps.users.repositories.converter import UserConverter


def test_user_converter_to_entity(user_factory):
    model = user_factory.build(
        pk=1,
        username='Tes_user',
        first_name='testing',
        last_name='tested',
        email='test@example.com',
        is_active=True,
        is_staff=False,
    )

    entity = UserConverter.to_entity(model=model)

    assert isinstance(entity, UserEntity)
    assert entity.id == model.pk
    assert entity.username == model.username
    assert entity.first_name == model.first_name
    assert entity.last_name == model.last_name
    assert entity.full_name == model.full_name
    assert entity.email == model.email
    assert entity.is_active == model.is_active
    assert entity.is_staff == model.is_staff
    assert entity.date_joined == model.date_joined
    assert isinstance(entity.date_joined, datetime)
