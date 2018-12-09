from .base import *

ALLOWED_HOSTS = ['localhost']

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': '127.0.0.1',
        'PASSWORD': 'test123'
    }
}
