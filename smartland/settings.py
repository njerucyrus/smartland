"""
Django settings for smartland project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cff&mf*zt#6^*xm1=6r_#-xm&(88!g2bq_f2158%ziatvq1pne'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'land',
    'payments',
    'api',
    'bootstrap3',
    'crispy_forms',
    'paypal.standard.ipn',
    'gunicorn',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'smartland.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
             'debug': DEBUG,
        },
    },
]


WSGI_APPLICATION = 'smartland.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smartland_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media_files/')

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static_root')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static_files'),
)

# heroku settings
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# django paypal configurations
PAYPAL_RECEIVER_EMAIL = 'njerucyrusdev@gmail.com'
#turn this off when you go to live account
PAYPAL_TEST = True

SAND_BOX = True
# AT credentials
if SAND_BOX:

    USERNAME = 'njerucyrus123'

    API_KEY = 'ff899257e3379a6f1d2cd734f7531ab7e1db7af7a872bb6e4a0255cfdba7b0cd'

    PRODUCT_NAME = 'SmartLand'

    CURRENCY_CODE = 'KES'

    METADATA = {}

else:

    AWS_QUERYSTRING_AUTH = True

    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

    MEDIA_URL = 'http://%s.s3.amazonaws.com/media_root/' % AWS_STORAGE_BUCKET_NAME

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"


    USERNAME = os.environ['AT_USERNAME']

    API_KEY = os.environ['API_KEY']

    PRODUCT_NAME = os.environ['PRODUCT_NAME']

    CURRENCY_CODE = os.environ['CURRENCY_CODE']

    METADATA = {}