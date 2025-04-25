from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from apps.account.models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('-date_joined', )
    list_display = ('username', 'first_name', 'last_name', 'date_joined', 'is_staff', )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ordering = ('-user__date_joined', )
    list_display = ('c_email', 'c_name', 'birth_date', 'optin', )
    search_fields = ('user__email', 'user__first_name', 'user__last_name', )
    raw_id_fields = ('user', )

    @admin.display(description=_('E-mail'))
    def c_email(self, obj):
        return obj.user.email

    @admin.display(description=_('Name'))
    def c_name(self, obj):
        return mark_safe(
            f'<a href="/admin/dj_account/user/{obj.user.id}/change/">'
            f'{obj.user.get_full_name()}'
            '</a>'
        )
