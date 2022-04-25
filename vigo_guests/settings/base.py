"""
Django settings for vigo_guests project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import ldap
from django_auth_ldap.config import LDAPSearch
from django_auth_ldap.config import NestedActiveDirectoryGroupType
import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a1@u+((7+uk%e9^p69061#5lykrsleazjfewd2sp#6lk03p&wh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.11.24']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "channels",
    'rest_framework',
    "interfaces",
    "api",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vigo_guests.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vigo_guests.wsgi.application'
ASGI_APPLICATION = 'vigo_guests.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

INTERNAL_IPS = [
    "127.0.0.1",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vigo_guests',
        'USER': 'postgres',
        'PASSWORD': 'wLFaEwHIRCfWBTY9rU9gNsEIZ',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channel_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)]
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# LDAP AD

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",

    # uncomment to work with AD
    # "django_auth_ldap.backend.LDAPBackend", 
]
AUTH_LDAP_SERVER_URI = "ldap://192.168.11.4:389"

AUTH_LDAP_BIND_DN = "CN=lister,OU=WsparcieUsers,OU=Users,OU=Vigo,DC=ad,DC=vigo,DC=com,DC=pl"
AUTH_LDAP_BIND_PASSWORD = "!Wsparcie5005"
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "OU=Users,OU=Vigo,DC=ad,DC=vigo,DC=com,DC=pl", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"
)
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "sAMAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "CN=aplikacja_recepcja,OU=WsparcieGroups,OU=Groups,OU=Vigo,DC=ad,DC=vigo,DC=com,DC=pl", ldap.SCOPE_SUBTREE
)
AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType(name_attr="cn")
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_superuser": "CN=aplikacja_recepcja_admin,OU=WsparcieGroups,OU=Groups,OU=Vigo,DC=ad,DC=vigo,DC=com,DC=pl",
    "is_staff": "CN=aplikacja_recepcja,OU=WsparcieGroups,OU=Groups,OU=Vigo,DC=ad,DC=vigo,DC=com,DC=pl",
}
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 1

LOGIN_URL = "/admin/login/"
LOGOUT_REDIRECT_URL = "/"
# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
