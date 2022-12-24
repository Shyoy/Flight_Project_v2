from .base import *

DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = 'django-insecure-zfuoe$wt+&6@xsg)8^^kcm5r(s6o_1)y!d7t3h*qv=^2e_qsyw'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}