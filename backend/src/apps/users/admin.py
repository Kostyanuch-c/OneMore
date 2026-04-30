from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):  # type: ignore[type-arg]
    model = User

    list_display = (
        'id',
        'username',
        'email',
        'is_superuser',
        'last_login',
        'date_joined',
    )
    list_filter = (
        'is_superuser',
        'is_active',
        'date_joined',
    )
    search_fields = (
        'username',
        'email',
    )
    ordering = ('-date_joined',)
    empty_value_display = '-пусто-'
    readonly_fields = ('date_joined', 'last_login')
