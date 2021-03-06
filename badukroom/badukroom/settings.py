"""
Django settings for badukroom project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf.global_settings import STATICFILES_DIRS, MEDIA_ROOT, MEDIA_URL
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e4&$ul9*^m3=sibt#b^k%bz$13amby0+lsvu)ako(f^-$%sl4n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'principal',
    'login',
    'redsocial',
    'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'badukroom.urls'

WSGI_APPLICATION = 'badukroom.wsgi.application'


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

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-ES'

#TIME_ZONE = 'UTC'
TIME_ZONE='Europe/Madrid' #CAMBIADO POR MI PARA LA HORA DE LOS COMENTARIOS AL CREARLAS EN JAVASCRIPT APARECIAN CON UNA HORA MENOS
USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

#add por mi
STATICFILES_DIRS = (
                    os.path.join(BASE_DIR, 'static'),
                    )
#fin add por mi

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

#add por me
#MEDIA_ROOT='/home/fla2727/workspace/tfg/badukroom/static/sgf' # seguardaran en esa carpeta y para visualizar en el template --> data-wgo="{% static 'sgf/kymco-ersev.sgf' %}"
#MEDIA_ROOT='/home/fla2727/workspace/tfg/badukroom/static/' # seguardaran en esa carpeta y para visualizar en el template --> data-wgo="{% static 'sgf/kymco-ersev.sgf' %}"
MEDIA_ROOT=os.path.join(BASE_DIR, 'media')
MEDIA_URL='/media/' # para descargar un sgf --> http://127.0.0.1:8000/media/ersev-butsimple

#MODIFICACIONES PARA ENVIAR email
# EMAIL SETTINGS
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "badukroom@gmail.com"
EMAIL_HOST_PASSWORD = "badukroomtfg"
EMAIL_USE_TLS = True