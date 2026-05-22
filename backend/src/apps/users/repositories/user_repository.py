from django.contrib.auth import get_user_model
from django.db.models import Q

from apps.users.dto import UserUpdateDTO
from apps.users.entities import (
    UserEntity,
)
from apps.users.repositories.converter import UserConverter


class UserRepository:
    user_model = get_user_model()
    converter = UserConverter

    def get_users_count(self, *, filters: Q | None = None) -> int:
        return self.user_model.objects.filter(filters or Q()).count()

    def get_users_list(
        self, *, filters: Q, limit: int, offset: int
    ) -> list[UserEntity]:
        return [
            self.converter.to_entity(model=user)
            for user in self.user_model.objects.filter(filters).order_by(
                '-date_joined'
            )[offset : offset + limit]
        ]

    def get_user_by_email(
        self, *, email: str, include_inactive: bool = False
    ) -> UserEntity | None:
        query = Q(email__iexact=email)
        if not include_inactive:
            query &= Q(is_active=True)

        user = self.user_model.objects.filter(query).first()

        return (
            self.converter.to_entity(model=user) if user is not None else None
        )

    def create_user(self, *, username: str, email: str) -> UserEntity:
        user = self.user_model(
            username=username,
            email=email,
        )
        user.set_unusable_password()
        user.save()
        return self.converter.to_entity(model=user)

    def update_user(
        self, *, user_id: int, user_data: UserUpdateDTO
    ) -> UserEntity:
        user_instance = self.user_model.objects.get(id=user_id)

        for key, value in user_data.to_update_dict().items():
            setattr(user_instance, key, value)

        user_instance.save()
        return self.converter.to_entity(model=user_instance)
