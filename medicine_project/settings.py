"""
Django settings for medicine_project project.
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# Vercel & Deployment Hosts
VERCEL = config('VERCEL', default=os.environ.get('VERCEL', ''))
VERCEL_URL = config('VERCEL_URL', default=os.environ.get('VERCEL_URL', ''))
RAILWAY_PUBLIC_DOMAIN = config('RAILWAY_PUBLIC_DOMAIN', default=None)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver', '.vercel.app', '.now.sh']
CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app']

if VERCEL_URL:
    ALLOWED_HOSTS.append(VERCEL_URL)
    CSRF_TRUSTED_ORIGINS.append(f'https://{VERCEL_URL}')

if RAILWAY_PUBLIC_DOMAIN:
    ALLOWED_HOSTS.extend([RAILWAY_PUBLIC_DOMAIN, '.railway.app'])
    CSRF_TRUSTED_ORIGINS.extend([f'https://{RAILWAY_PUBLIC_DOMAIN}', 'https://*.railway.app'])

# Custom ALLOWED_HOSTS from env
custom_hosts = config('ALLOWED_HOSTS', default='')
if custom_hosts:
    for h in custom_hosts.split(','):
        h = h.strip()
        if h:
            ALLOWED_HOSTS.append(h)
            if not h.startswith('.'):
                CSRF_TRUSTED_ORIGINS.append(f'https://{h}')



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recommendation',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'medicine_project.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'medicine_project.wsgi.application'



# Database configuration
database_url = config('DATABASE_URL', default=os.environ.get('DATABASE_URL', ''))
db_name = config('DB_NAME', default=None)

if database_url:
    is_sqlite = database_url.strip().startswith('sqlite')
    DATABASES = {
        'default': dj_database_url.parse(database_url, conn_max_age=0, ssl_require=not is_sqlite)
    }
elif db_name:
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE', default='django.db.backends.mysql'),
            'NAME': db_name,
            'USER': config('DB_USER', default=''),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='3306'),
        }
    }
else:
    # On Vercel, the filesystem is read-only except /tmp
    is_vercel = bool(VERCEL or VERCEL_URL or os.environ.get('VERCEL'))
    db_path = '/tmp/db.sqlite3' if is_vercel else (BASE_DIR / 'db.sqlite3')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_path,
        }
    }


# Password validation
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


# Internationalization
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('hi', 'हिन्दी'),
    ('mr', 'मराठी'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Language cookie settings
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = None  # Session cookie
LANGUAGE_COOKIE_PATH = '/'
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_SECURE = False
LANGUAGE_COOKIE_HTTPONLY = False
LANGUAGE_COOKIE_SAMESITE = 'Lax'

TIME_ZONE = 'UTC'

# Use signed cookie session engine for serverless speed and reliability
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise configuration for serving static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Logging configuration for debugging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
