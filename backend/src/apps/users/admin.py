from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        'id',
        'username',
        'email',
        'is_tutor',
        'is_staff',
        'last_login',
        'date_joined',
    )

    list_editable = ('is_tutor',)

    list_filter = (
        'is_superuser',
        'is_active',
        'is_tutor',
        'date_joined',
    )

    search_fields = (
        'username',
        'email',
    )

    ordering = ('-date_joined',)
    empty_value_display = '-пусто-'
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = BaseUserAdmin.fieldsets + (  # type: ignore[operator]
        (
            'Роль пользователя',
            {'fields': ('is_tutor',)},
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            'Роль пользователя',
            {'fields': ('is_tutor',)},
        ),
    )
