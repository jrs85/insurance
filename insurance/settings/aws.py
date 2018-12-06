import os

from .base import *

MIDDLEWARE.append(
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
WHITENOISE_STATIC_PREFIX = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('RDS_DB_NAME'),
        'USER': os.getenv('RDS_DB_USER'),
        'HOST': os.getenv('RDS_DB_HOST'),
        'PASSWORD': os.getenv('RDS_DB_PASSWORD'),
    }
}
