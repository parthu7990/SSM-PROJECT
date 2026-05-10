"""
Django settings for PSK Future Innovation FZE
Production-ready with Cloudinary + Render support
"""

from pathlib import Path
from decouple import config, Csv
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ───────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='django-insecure-psk-change-in-production-2026')
DEBUG      = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())

# ── Apps ───────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'cloudinary_storage',
    'core',
    'custom_admin',
]

# ── Middleware ─────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # serve static on Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ssm_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'core.context_processors.company_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'ssm_config.wsgi.application'

# ── Database ───────────────────────────────────────────────
# Render provides DATABASE_URL env var automatically
DATABASE_URL = config('DATABASE_URL', default='')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ── Password Validation ────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalisation ───────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Dubai'
USE_I18N = True
USE_TZ   = True

# ── Static Files (WhiteNoise for Render) ──────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Cloudinary Media Storage ───────────────────────────────
CLOUDINARY_CLOUD_NAME = config('djy8vd01g', default='')
CLOUDINARY_API_KEY    = config('288547962925256',    default='')
CLOUDINARY_API_SECRET = config('deDJYSmdFv0DehzRXtmGCfKWYfU', default='')

if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
    # Use Cloudinary for ALL media uploads
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
        'API_KEY':    CLOUDINARY_API_KEY,
        'API_SECRET': CLOUDINARY_API_SECRET,
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = f'https://res.cloudinary.com/{CLOUDINARY_CLOUD_NAME}/'
else:
    # Fallback to local storage (development)
    MEDIA_URL  = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Email ──────────────────────────────────────────────────
EMAIL_BACKEND      = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST         = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT         = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS      = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER    = config('EMAIL_HOST_USER', default='info@pskfutureinnovation.com')
EMAIL_HOST_PASSWORD= config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='info@pskfutureinnovation.com')
ADMIN_EMAIL        = config('ADMIN_EMAIL', default='info@pskfutureinnovation.com')

# ── Security (production) ──────────────────────────────────
if not DEBUG:
    SECURE_PROXY_SSL_HEADER    = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT        = True
    SESSION_COOKIE_SECURE      = True
    CSRF_COOKIE_SECURE         = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF= True
    X_FRAME_OPTIONS            = 'DENY'
