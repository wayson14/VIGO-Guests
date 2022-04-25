from .base import *

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

ALLOWED_HOSTS = ['192.168.11.24']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}