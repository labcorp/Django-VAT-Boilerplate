import os

from django.conf import settings
from conf.settings.base import ENV


DJANGO_VITE = {
    'default': {
        'dev_mode': ENV.bool('DEBUG'),
        'manifest_path': os.path.join(settings.STATIC_DEV if ENV('DEBUG') else settings.STATIC_ROOT, 'manifest.json')
    }
}
