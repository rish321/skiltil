"""
Django settings for projectX project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import raven
import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=swlc(#&pqqdr^$3kumc_ul4+072x(57(2g#jzd)6g7viws6$g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
	'proj.apps.ProjConfig',
	'customers.apps.CustomersConfig',
	'session.apps.SessionConfig',
	'payment.apps.PaymentConfig',
	'base.apps.BaseConfig',
	#'material',
        #'material.frontend',
        #'material.admin',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
    'social.apps.django_app.default',
	'raven.contrib.django.raven_compat',
	'analytical',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'projectX.urls'

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

                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    ('django.contrib.auth.backends.ModelBackend'),
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
)

WSGI_APPLICATION = 'projectX.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'projectX',
        'USER': 'rishabh',
        'PASSWORD': 'rishabh321',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static"),
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'proj.save_profile.save_profile',  # <--- set the path to the function
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

#AUTH_USER_MODEL = 'customers.Customer'
#SOCIAL_AUTH_USER_MODEL = 'customers.Customer'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'

SOCIAL_AUTH_CLEAN_USERNAMES = True


SOCIAL_AUTH_FACEBOOK_KEY = "1291723094225037"
SOCIAL_AUTH_FACEBOOK_SECRET = "53bb6c281e65d1f6a1255fb2c92a3dee"
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email,gender,link,age_range,',
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '863940487694-enr4digdlj451hr0dlondrjke5ar9h45.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '9VHRqu6ldRRcpl_jLqIOzYk5'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FILE_PATH = '~/Documents/app-messages' 
DEFAULT_FROM_EMAIL = 'help_skiltil@gmail.com'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'Skiltil'
EMAIL_HOST_PASSWORD = 'skilil19987'
#EMAIL_USE_TLS = False 
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#CLICKY_SITE_ID = '101008337'

#RAVEN_CONFIG = {
#	'dsn': 'https://41ec5e53e81f42a98a8c5f2de541fa94:c6e43498554a440f8cff16cc95a83417@sentry.io/119904',
#	# If you are using git, you can also automatically configure the
#	# release based on the git info.
#	'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
#}

#logger = logging.getLogger("sentry.errors")
#handler = logging.StreamHandler()
#formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
#handler.setFormatter(formatter)
#logger.addHandler(handler)
