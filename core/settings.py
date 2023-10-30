# -*- encoding: utf-8 -*-
"""

"""

import os, environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='S#perS3crEt_007')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Assets Management
ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets') 

# load production server from .env
ALLOWED_HOSTS        = ['localhost', 'localhost:85', '127.0.0.1', env('SERVER', default='127.0.0.1')]
CSRF_TRUSTED_ORIGINS = ['http://localhost:85', 'http://127.0.0.1', 'https://' + env('SERVER', default='127.0.0.1') ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.home',  # Enable the inner home (home)
    'users', 
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google' # for Google OAuth 2.0
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.context_processors.cfg_assets_root',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = { 
    'default': {
        'ENGINE'  : 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=public'
        }, 
        'NAME'    : os.getenv('DB_DASHBOARD_NAME'     ),
        'USER'    : os.getenv('DB_DASHBOARD_USERNAME' ),
        'PASSWORD': os.getenv('DB_DASHBOARD_PASS'     ),
        'HOST'    : os.getenv('DB_DASHBOARD_HOST'     ),
        'PORT'    : os.getenv('DB_DASHBOARD_PORT'     ),
    },
    'datamart_postgres': {
        'ENGINE'  : 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=mart_prd'
        },
        'NAME'    : os.getenv('DB_POSTGRE_NAME'     ),
        'USER'    : os.getenv('DB_POSTGRE_USERNAME' ),
        'PASSWORD': os.getenv('DB_POSTGRE_PASS'     ),
        'HOST'    : os.getenv('DB_POSTGRE_HOST'     ),
        'PORT'    : os.getenv('DB_POSTGRE_PORT'     ),
    },
    'airflow': {
        'ENGINE'  : 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=public'
        },
        'NAME'    : os.getenv('DB_AIRFLOW_NAME'     ),
        'USER'    : os.getenv('DB_AIRFLOW_USERNAME' ),
        'PASSWORD': os.getenv('DB_AIRFLOW_PASS'     ),
        'HOST'    : os.getenv('DB_AIRFLOW_HOST'     ),
        'PORT'    : os.getenv('DB_AIRFLOW_PORT'     ),
    },
    'klopos': {
        'ENGINE'  : 'django.db.backends.mysql',
        'NAME'    : os.getenv('DB_KLOPOS_NAME'     ),
        'USER'    : os.getenv('DB_KLOPOS_USERNAME' ),
        'PASSWORD': os.getenv('DB_KLOPOS_PASS'     ),
        'HOST'    : os.getenv('DB_KLOPOS_HOST'     ),
        'PORT'    : os.getenv('DB_KLOPOS_PORT'     ),
    },
}

ENV = os.getenv('ENV')

AIRFLOW_ENDPOINT = os.getenv('AIRFLOW_ENDPOINT')
AIRFLOW_USERNAME = os.getenv('AIRFLOW_USERNAME')
AIRFLOW_PASSWORD = os.getenv('AIRFLOW_PASSWORD')

NIFI_ENDPOINT = os.getenv('NIFI_ENDPOINT')
NIFI_USERNAME = os.getenv('NIFI_USERNAME')
NIFI_PASSWORD = os.getenv('NIFI_PASSWORD')

KAFKA_ENDPOINT = os.getenv('KAFKA_ENDPOINT')

ETL_ENDPOINT = os.getenv('ETL_ENDPOINT')
ETL_ENDPOINT_AKUNTING = os.getenv('ETL_ENDPOINT_AKUNTING')

VALIDITY_ENDPOINT = os.getenv('VALIDITY_ENDPOINT')

COCKPIT_ENDPOINT = os.getenv('COCKPIT_ENDPOINT')
COCKPIT_USERNAME = os.getenv('COCKPIT_USERNAME')
COCKPIT_PASSWORD = os.getenv('COCKPIT_PASSWORD')


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

# Additional configuration settings
ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET=True
ACCOUNT_LOGOUT_ON_GET= True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

AUTH_USER_MODEL = 'users.User'

#DATABASE ROUTE
# DATABASE_ROUTERS = ['core.route.DatamartRouter']

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)


#############################################################
#############################################################
