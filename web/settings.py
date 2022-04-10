"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
from pathlib import Path
from environ import Env
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = Env()
env.read_env(env_file='web/.env')
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '3$!e5*ggej1g%8n!d77u^5jk$qy&_p_6r_gc2+mdu(2v1-&c%@'

SECRET_KEY = env('DJANGO_SECRET_KEY', default = '3$!e5*ggej1g%8n!d77u^5jk$qy&_p_6r_gc2+mdu(2v1-&c%@')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

DEBUG = env('DJANGO_DEBUG', default=True)

# ALLOWED_HOSTS = []
# ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'eventify.apps.EventifyConfig',
    'crispy_forms',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'location_field.apps.DefaultConfig',
    'star_ratings',
    'django.contrib.sites',
    'actstream', 
    'django_jsonfield_backport'
  
]
STAR_RATINGS_CLEARABLE = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware'
]


ROOT_URLCONF = 'web.urls'

LOCATION_FIELD = {
    'provider.google.api': '//maps.google.com/maps/api/js?sensor=false',
    'provider.google.api_key': 'AIzaSyCZpVlHNcseo02s65Ue8NpZYQGRCIwaMKo',
    'provider.google.api_libraries': '',
    'provider.google.map.type': 'ROADMAP',
}
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

WSGI_APPLICATION = 'web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {

      'default': {
        'ENGINE': env('DB_ENGINE', default = 'django.db.backends.postgresql_psycopg2'),
        'NAME': env('DB_NAME', default='eventifydb'), 
        'USER': env('DB_USER', default='postgres'), 
        # 'PASSWORD': env('DB_PASSWORD', default='Pass1234'),
        'PASSWORD': env('DB_PASSWORD', default='q1w2e3'),
        'HOST': env('DB_HOST', default='127.0.0.1'), 
        # 'HOST': env('DB_HOST'), 
        'PORT': env('DB_PORT', default='5432'),
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': 'db.sqlite3', # This is where you put the name of the db file. 
    #              # If one doesn't exist, it will be created at migration time.
    # }
}

CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS").split(" ")

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static-cdn')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'web/static')
]


# Media Files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Crispy Settings

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Authentication Settings

LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'login'

# Email Settings

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 1

ACTSTREAM_SETTINGS = {
    'MANAGER': 'web.managers.MyActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}
