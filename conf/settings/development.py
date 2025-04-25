# pylint: disable=W0614, W0401
from conf.settings.base import *
from conf.settings.project import *


DEBUG = ENV.bool("DEBUG", True)
PTVSD_SERVER = ENV.bool("PTVSD_SERVER", True)

ALLOWED_HOSTS = ['*', ]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + PROJECT_APPS
