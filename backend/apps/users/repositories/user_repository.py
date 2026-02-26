from django.contrib.auth import get_user_model
from django.db.models import Q

from api.v1.users.schemas import UserUpdateSchema
from apps.users.entities import (
    UserEntity,
)
from apps.users.repositories.converter import UserConverter


class UserRepository:
    user_model = get_user_model()
    converter = UserConverter

    EMAIL_CONSTRAINT = 'uniq_user_email_when_present'
    USERNAME_CONSTRAINT = 'uniq_user_username'

    def is_username_free(
        self,
        username: str,
        user_id: int | None = None,
    ) -> bool:
        return not self.user_model.objects.filter(
            Q(username=username) & ~Q(id=user_id),
        ).exists()

    def is_email_free(self, email: str) -> bool:
        return not self.user_model.objects.filter(email__iexact=email).exists()

    def get_users_count(self) -> int:
        return self.user_model.objects.count()

    def get_all_users(self) -> list[UserEntity]:
        return [
            self.converter.to_entity(user)
            for user in self.user_model.objects.all()
        ]

    def get_user_by_id(self, user_id: int) -> UserEntity:
        return self.converter.to_entity(
            self.user_model.objects.get(id=user_id),
        )

    def create_user(
        self,
        password: str,
        username: str,
        email: str | None = None,
    ) -> UserEntity:
        return self.converter.to_entity(
            self.user_model.objects.create_user(
                password=password,
                username=username,
                email=email,
            ),
        )

    def update_user(
        self,
        user_id: int,
        user_data: UserUpdateSchema,
    ) -> UserEntity:
        user_instance = self.user_model.objects.get(id=user_id)

        update_data = user_data.dict(exclude_unset=True)
        password = update_data.pop('password', None)
        if password:
            user_instance.set_password(password)

        for key, value in update_data.items():
            setattr(user_instance, key, value)

        user_instance.save()
        return self.converter.to_entity(user_instance)

    def delete_object(self, user_id: int) -> None:
        self.user_model.objects.filter(id=user_id).delete()
