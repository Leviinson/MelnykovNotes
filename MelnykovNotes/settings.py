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
from .typehints import Period
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wowowowo!!!!itstheMostDIFfuCULTCodeThat1Ha533ver8een'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1']


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
    'userprofile.apps.UserprofileConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'caching'),
    }
}


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
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '| [{levelname}] — [{asctime}] — [{module}] | \n {message} \n' + '-'*100,
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'userprofile_log_handler': {
            'level':'DEBUG' if DEBUG else 'WARNING',
            'class':'logging.FileHandler',
            'filename': 'userprofile.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        },
        'userprofile': {
            'handlers': ['userprofile_log_handler'],
        }
    },
    'root': {
        'handlers': ['userprofile_log_handler'],
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
# key value "relativedelta_parameter_title" is using to pass parameter for dateutil.relativedelta func,
# so it can raise errors if you change it, but you can change "all_time" key values.
THIS_DAY_PERIOD = Period(abbreviature = "td",
                         title = "day",
                         relativedelta_parameter_title = "days",
                         django_template__date_filter = "j F",
                         django_orm_date_truncation = "day")

THIS_WEEK_PERIOD = Period(abbreviature = "tw",
                          title = "week",
                          relativedelta_parameter_title = "weeks",
                          django_template__date_filter = "j F",
                          django_orm_date_truncation = "day")

THIS_MONTH_PERIOD = Period(abbreviature = "tm",
                           title = "month",
                           relativedelta_parameter_title = "months",
                           django_template__date_filter = "j F",
                           django_orm_date_truncation = "day")

THIS_YEAR_PERIOD = Period(abbreviature = "ty",
                          title = "year",
                          relativedelta_parameter_title = "years",
                          django_template__date_filter = "F",
                          django_orm_date_truncation = "month")

ALL_TIME_PERIOD = Period(abbreviature = "at",
                         title = "all time",
                         django_template__date_filter = "Y",
                         django_orm_date_truncation = "year")

DICT_OF_PERIODS = {
    THIS_DAY_PERIOD.abbreviature: THIS_DAY_PERIOD,
    THIS_WEEK_PERIOD.abbreviature: THIS_WEEK_PERIOD,
    THIS_MONTH_PERIOD.abbreviature: THIS_MONTH_PERIOD,
    THIS_YEAR_PERIOD.abbreviature: THIS_YEAR_PERIOD,
    ALL_TIME_PERIOD.abbreviature: ALL_TIME_PERIOD
    }
DEFAULT_PERIOD = THIS_DAY_PERIOD

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
