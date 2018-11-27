from .base import *

MIDDLEWARE.append(
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
WHITENOISE_STATIC_PREFIX = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
