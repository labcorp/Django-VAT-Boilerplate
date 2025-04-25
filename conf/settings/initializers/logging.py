import os
import logging.config

from django.utils.log import DEFAULT_LOGGING
from conf.settings.base import ROOT_DIR

from apps.core.utils.log import logging_formats


# Levels
#
# DEBUG: Low level system information for debugging purposes
# INFO: General system information
# WARNING: Information describing a minor problem that has occurred.
# ERROR: Information describing a major problem that has occurred.
# CRITICAL: Information describing a critical problem that has occurred.

LOGGING_CONFIG = None

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': logging_formats.get('simple')
        },
        'full': {
            'format': logging_formats.get('full')
        },
        'colored_simple': {
            '()': 'apps.core.utils.log.ColoredFormatter',
            'format': logging_formats.get('simple')
        },
        'colored_full': {
            '()': 'apps.core.utils.log.ColoredFormatter',
            'format': logging_formats.get('full')
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server']
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console_simple': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true', ],
            'formatter': 'colored_simple',
        },
        'console_full': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true', ],
            'formatter': 'colored_full',
        },
        'file': {
            'level': 'INFO',
            'filename': os.path.join(ROOT_DIR, '_logs/application.log'),
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5, # 5MB
            'backupCount': 5,
            'formatter': 'full',
        },
        'database': {
            'level': 'WARNING',
            'filters': ['require_debug_false', ],
            'class': 'apps.core.utils.log.DBHandler',
            'formatter': 'full'
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'cms': {
            'level': 'DEBUG',
            'handlers': ['console_full', 'file', 'database', ],
            'propagate': False
        },
        'django': {
            'level': 'WARNING',
            'handlers': ['database', 'console_full', 'file', ],
            'propagate': False
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
})
