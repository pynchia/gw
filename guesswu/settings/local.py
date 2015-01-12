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
        'NAME': 'guesswu',
        'USER': 'intranet',
        'PASSWORD': 'xyzxyz',
        'HOST': '192.168.3.10',
        'PORT': '',
    }
}

INSTALLED_APPS += ("debug_toolbar", )
INTERNAL_IPS = ("127.0.0.1",)
MIDDLEWARE_CLASSES += \
        ("debug_toolbar.middleware.DebugToolbarMiddleware", )

