from .base import *

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}

"""
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]


#move to base in future
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vigo-guests',
        'USER': 'postgres',
        'PASSWORD': 'wLFaEwHIRCfWBTY9rU9gNsEIZ',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""