import os
from conf.settings.base import ENV

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

db = ENV.db()

DATABASES = {
    'default': db
}
