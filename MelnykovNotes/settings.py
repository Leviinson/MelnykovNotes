"""
Django settings for MelnykovNotes project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--wn*owr84kqkg_bd83-_vjo5j^f9ohdgsq7(tp0_0d(s@87@y)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authorization.apps.AuthorizationConfig',
    'about.apps.AboutConfig',
    'news.apps.NewsConfig',
    'userprofile.apps.UserprofileConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MelnykovNotes.urls'

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

WSGI_APPLICATION = 'MelnykovNotes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_TITLE'),
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD')
        }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'authorization.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# REDIRECTS URLS
# https://docs.djangoproject.com/en/4.1/ref/settings/#login-url
# https://docs.djangoproject.com/en/4.1/ref/settings/#login-redirect-url

LOGIN_URL = 'authentication'

# Media files (MEDIA_ROOT, MEDIA_URL)
# https://docs.djangoproject.com/en/4.1/ref/settings/#media-root
# https://docs.djangoproject.com/en/4.1/ref/settings/#media-url

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# USER PROFILE PAGE SETTINGS

# "abbreviature" key is using to represent value for parameter "period_abbreviature"
# in "userprofile:profile_page" URLconf path.

# "title" key is using to represent period title on userprofile page  

# If you want to change 'all_time' key, so also
# pass changes for those requirements:
#     userprofile/services.py/_define_period_parameter_for_relativedelta (func)

# You can change only "abbreviature", "all_time", and "title" key values,
# key value "__parameter_title" is using to pass parameter for dateutil.relativedelta func,
# so it can raise errors if you change it, but you can change "all_time" key values.
THIS_DAY_PERIOD = {
    "abbreviature": "td",
    "title": "day",
    "__parameter_title": "days"
}
THIS_WEEK_PERIOD = {
        "abbreviature": "tw",
        "title": "week",
        "__parameter_title": "weeks"
    }
THIS_MONTH_PERIOD = {
        "abbreviature": "tm",
        "title": "month",
        "__parameter_title": "months"
    }
THIS_YEAR_PERIOD = {
        "abbreviature": "ty",
        "title": "year",
        "__parameter_title": "years"
    }
ALL_TIME_PERIOD = {
        "abbreviature": "at",
        "title": "all time",
    }
DICT_OF_PERIODS = {
    THIS_DAY_PERIOD['abbreviature']: THIS_DAY_PERIOD,
    THIS_WEEK_PERIOD['abbreviature']: THIS_WEEK_PERIOD,
    THIS_MONTH_PERIOD['abbreviature']: THIS_MONTH_PERIOD,
    THIS_YEAR_PERIOD['abbreviature']: THIS_YEAR_PERIOD,
    ALL_TIME_PERIOD['abbreviature']: ALL_TIME_PERIOD
}
DEFAULT_PERIOD = THIS_DAY_PERIOD
