from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountConfig(AppConfig):
    name = 'apps.account'
    label = 'dj_account'
    verbose_name = _('account')
    verbose_name_plural = _('account')
