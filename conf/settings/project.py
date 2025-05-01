# pylint: disable=unused-wildcard-import, wildcard-import
import os

from conf.settings.base import ENV, ROOT_DIR, TEMPLATES

from conf.settings.initializers.database import *
from conf.settings.initializers.restframework import *
from conf.settings.initializers.logging import *
from conf.settings.initializers.vite import *
from conf.settings.initializers.tinymce import *
from conf.settings.initializers.filer import *
from conf.settings.initializers.thumbnails import *
from conf.settings.initializers.cotton import *


PROJECT_NAME = 'Awesome Project'
SECRET_KEY = ENV('SECRET_KEY')
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(ROOT_DIR, '_emails'),

EXTERNAL_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'django_extensions',
    'django_vite',
    'djangoql',
    'django_cotton.apps.SimpleAppConfig',
    'filer',
    'easy_thumbnails',
    'tinymce',
    'adminsortable2',
]

PROJECT_APPS = [
    'apps.core.apps.CoreConfig',
    'apps.account.apps.AccountConfig', # Custom User Model
    'apps.web.apps.WebConfig',
    'apps.content.apps.ContentConfig',
]

TEMPLATES[0]['OPTIONS']['context_processors'].append('apps.core.context_processors.globals')
