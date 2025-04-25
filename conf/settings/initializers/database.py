import os
from conf.settings.base import ENV

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

db = ENV.db()
dockered = os.environ.get('DOCKERED', False)

if dockered:
    db['HOST'] = 'db'

DATABASES = {
    'default': db
}
