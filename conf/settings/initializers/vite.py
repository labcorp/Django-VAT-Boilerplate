from django.conf import settings
from conf.settings.base import ENV


DJANGO_VITE = {
    'default': {
        'dev_mode': ENV.bool('DEBUG')
    }
}
