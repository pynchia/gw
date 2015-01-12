# settings/local.py
from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': get_env_variable("DJANGO_DB_HOST"),
        'NAME': get_env_variable("DJANGO_DB_NAME"),
        'USER': get_env_variable("DJANGO_DB_USER"),
        'PASSWORD': get_env_variable("DJANGO_DB_PWD"),
        'PORT': '',
    }
}

INSTALLED_APPS += ("debug_toolbar", )
INTERNAL_IPS = ("127.0.0.1",)
MIDDLEWARE_CLASSES += \
        ("debug_toolbar.middleware.DebugToolbarMiddleware", )

