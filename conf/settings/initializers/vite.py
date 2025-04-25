from django.conf import settings
from conf.settings.base import ENV


DJANGO_VITE = {
    'default': {
        'dev_mode': ENV('DEBUG'),
        'manifest_path': settings.STATIC_DEV if ENV('DEBUG') else settings.STATIC_ROOT
    }
}
