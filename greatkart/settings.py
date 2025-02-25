"""
Django settings for greatkart project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

from django.utils.translation import gettext_lazy as _
#from django.utils.translation import gettext_lazy as _


# importer decouple afin de pouvoir appeler les variabkes secretes
from decouple import config
import dj_database_url

# installer : pip install psycopg2



# il faut installer decouple avec la commande :     pip install python-decouple
 # pour la securite de notre site

#from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

#ALLOWED_HOSTS = ["AfriShop.pythonanywhere.com"]

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages", # django permet de gerer les messages
    "django.contrib.staticfiles",
    "category",
    "accounts",
    "store",
    "carts",
    "orders",
    #'admin_honeypot', # installee avec la commande  :   pip install django-admin-honeypot


]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django_session_timeout.middleware.SessionTimeoutMiddleware', #installer avec la commande pour la deconnexion automatique: pip install django-session-timeout
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Ajoutez cette ligne pour que render puisse prendre en compte les fichiers statics


]

# Pour la deconnexion automatique
SESSION_EXPIRE_SECONDS = 3600  # on definit le temps qu'inactivite de l'utilisateur sur le site
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True # on valide sa deconnexion
SESSION_TIMEOUT_REDIRECT = '/accounts/login' # on  le redirige vers la page de connexion


import cloudinary
import cloudinary.uploader
import cloudinary.api

import os

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME'),
    'API_KEY': os.getenv('API_KEY'),
    'API_SECRET': os.getenv('API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Configuration pour WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ROOT_URLCONF = "greatkart.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates'], # that I add
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "category.context_processor.menu_links",# ce que nous avons ajouter pour qu'il soit accessible partout
                "carts.context_processors.counter", # nous l'avons ajouter pour qu'il soit accessible partout
            ],
        },
    },
]

WSGI_APPLICATION = "greatkart.wsgi.application"
AUTH_USER_MODEL ='accounts.Account'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": "ecommerce",
#         "USER": "fiarma",
#         "PASSWORD": "fiarma",
#         "HOST": "localhost",
#         "PORT": "5432",


#     }
# }

DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL'))
}

# Pour les emails

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAAIL_PORT = config('EMAAIL_PORT')


# CREATE DATABASE ecommerce;
# CREATE USER fiarma WITH PASSWORD 'fiarma';
# GRANT ALL PRIVILEGES ON DATABASE ecommerce TO fiarma;

# psql -U fiarma -d ecommerce -h 127.0.0.1 -W





# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
# Ce que j'ajoute
#STATIC_ROOT = BASE_DIR/'static'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
    #'greatkart/static'
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


#cConfiguration des fichiers  media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR /'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Pour la gestion des messages
from django.contrib.messages import constants as messages
MESSAGES_TAGS={
    messages.ERROR: 'danger'
}

import django


from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str
# Cette partie concerne l'envoi du mail






