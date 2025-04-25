# pylint: disable=W0614, W0401
from conf.settings.base import *
from conf.settings.project import *


DEBUG = ENV.bool("DEBUG", False)
PTVSD_SERVER = ENV.bool("PTVSD_SERVER", False)

ALLOWED_HOSTS = ['*', ]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + PROJECT_APPS
