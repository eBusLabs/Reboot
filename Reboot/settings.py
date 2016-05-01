"""
Django settings for Reboot project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import STATICFILES_DIRS  # @UnusedImport
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Reboot',
    'logon',
    'app_user_home',
    'app_poll_core',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'Reboot.mymiddleware.RestrictStaffToAdminMiddleware',
)

ROOT_URLCONF = 'Reboot.urls'

WSGI_APPLICATION = 'Reboot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
 
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)
STATIC_URL = '/static/'
 
#Media Files
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

#Adding my template directory. I will use tuple
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug':DEBUG,
        },
    },
]

# Logging
# settings.py
APP_LOG_LEVEL='DEBUG'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'debugfile': {
            'level': APP_LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,'logs/debug.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['debugfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'Reboot': {
            'handlers': ['debugfile',],
            'propagate': True,
            'level': APP_LOG_LEVEL,
        },      
        'logon': {
            'handlers': ['debugfile',],
            'propagate': True,
            'level': APP_LOG_LEVEL,
        },
        'app_user_home': {
            'handlers': ['debugfile',],
            'propagate': True,
            'level': APP_LOG_LEVEL,
        },
        'app_user_core': {
            'handlers': ['debugfile',],
            'propagate': True,
            'level': APP_LOG_LEVEL,
        },             
                   
    }
}

#Change default login url
LOGIN_URL = '/logon/'

from .hushhush import *  # @UnusedWildImport
#hushhush.py contain secret data, create a hushhush.py and uncomment below line and change as per your need
#SECRET_KEY = '$[-)@J?Sn:C/!#E}PxHWH~4EkO`8OADtw:,7qPm#{>yFL'_58]'

#Email Settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = '587'
# EMAIL_HOST_USER = 'your email'
# DEFAULT_FROM_EMAIL =  EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD = 'your password'
# EMAIL_USE_TLS = True
