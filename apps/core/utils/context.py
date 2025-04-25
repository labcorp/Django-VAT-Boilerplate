from django.conf import settings
from conf.settings.base import ENV


def global_content(request):
    context = {
        'globals': {
        }
    }

    return context
