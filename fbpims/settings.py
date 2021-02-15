"""
Django settings for fbpims project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from django.conf import global_settings
import django.conf.locale
from django.db.models import JSONField

gettext_noop = lambda s: s


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u#@!ig3kcz)ocq=2791oii#ay4&$$6lxvj5!$cb2wkfhi5nt(q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.113','127.0.0.1','127.0.0.2']


# Application definition

INSTALLED_APPS = [
    'admin_site.apps.CustomAdminAppConfig',
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'admin_site',
    'accounts',
    'collaborations',
    'company',
    'product',
    'social_django',
    'colorfield',
    'crispy_forms',
    'django_summernote',
    'useraudit',
    'rest_framework',
    'rest_framework.authtoken',
 

]




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'fbpims.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'fbpims.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'admindb',
        'USER': 'postgres',
        'PASSWORD': 'cbe@ps4woga',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

EXTRA_LANG_INFO = {
    'am': {
        'bidi': False, # left-to-right
        'code': 'am',
        'name': 'Amharic',
        'name_local': u'አማሪኛ', #unicode codepoints here
    },
}

LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO

LANGUAGES = global_settings.LANGUAGES+ [('am', gettext_noop('Amharic')),]

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR,"locale"),
)

DATA_UPLAOD_MAX_MEMORY_SIZE = 10485864

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'assets'),
)
CRISPY_TEMPLATE_PACK = 'bootstrap4'


LOGIN_REDIRECT_URL = 'complete_login'
LOGOUT_REDIRECT_URL = 'login'
 
AUTH_USER_MODEL = 'accounts.User'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media/uploads/')

X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_THEME = 'bs4'


"""Email Related Settings"""
# For development use smtp EmailBackend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "email_archive")

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = "melkamu.aait@gmail.com"
EMAIL_HOST_PASSWORD = "0920854091"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_USE_LOCALTIME = True

#### For the RestFramework

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ]

# }




##### social-auth for postgres
JSONField = True

##### used by social-auth
AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)



SOCIAL_AUTH_FACEBOOK_KEY = '2860739290914734'  #APP ID
SOCIAL_AUTH_FACEBOOK_SECRET = '5afc8b24a3cdb7d93dcccf3fa06f49b6' #APP SECRET

##### Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '753998838053-1gd5boe4mjbvulm8cv71em8q0tf21k1v.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'd7UttVSC6u_KamtFI0_kY4RS'

SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]
#######


######  Github
SOCIAL_AUTH_GITHUB_KEY = '1e66719b28647a384cb2'  #CLIENT ID
SOCIAL_AUTH_GITHUB_SECRET = '271b0d0d47b41342933f5f8287f43f0f2d3eb070' #CLIENT SECRET
######
