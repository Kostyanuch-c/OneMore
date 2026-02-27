from django.http import Http404

from api.v1.users.schemas import UserUpdateSchema
from apps.common.error_handlers import handle_unique_field
from apps.users.entities import (
    UserEntity,
)
from apps.users.models import User
from apps.users.repositories.user_repository import UserRepository


class UserService:
    repository = UserRepository()

    def get_users_count(self) -> int:
        return self.repository.get_users_count()

    def get_all_objects(self) -> list[UserEntity]:
        return self.repository.get_all_users()

    def get_user(self, user_id: int) -> UserEntity:
        try:
            return self.repository.get_user_by_id(user_id)
        except User.DoesNotExist:
            raise Http404

    @handle_unique_field(
        field='username',
        check_exist_func=repository.is_username_free,
        data_index=0,
        id_index=0,
    )
    def update_user(
        self,
        user_id: int,
        user_data: UserUpdateSchema,
    ) -> UserEntity:
        return self.repository.update_user(user_id, user_data)

    def delete_user(self, user_id: int) -> None:

        return self.repository.delete_object(user_id)
