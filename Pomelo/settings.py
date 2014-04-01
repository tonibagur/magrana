"""
Django settings for Pomelo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
gettext = lambda s: s
PROJECT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')^ht%%o2#qo%qrat=&puf3u&39ez16a-tc)dt6p#5zbrhp_07='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'djangocms_admin_style', #for the admin skin. You must add 'djangocms_admin_style' in the list before 'django.contrib.admin'.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django CMS
    'djangocms_text_ckeditor', # note this needs to be above the 'cms' entry
    'cms', # django CMS itself
    'cms.stacks', # for reusable content
    'mptt', #utilities for implementing a modified pre-order traversal tree
    'menus', # helper for model independent hierarchical website navigation
    'south', # intelligent schema and data migrations
    'sekizai', # for javascript and css management
    'widget_tweaks',

    # youtube
    'django_youtube',
    'widget_tweaks',

    'djangular',

    'Pomelo',
)

MIDDLEWARE_CLASSES = (

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

ROOT_URLCONF = 'Pomelo.urls'

WSGI_APPLICATION = 'Pomelo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pomelo',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates")
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    #'cms.context_processors.cms_settings',
    'sekizai.context_processors.sekizai',
)

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "static")

MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")
MEDIA_URL = "/media/"

CMS_TEMPLATES = (
    ('empty.html', 'Empty Template'),
)

LANGUAGES = [
    ('en', 'English'),
]

SITE_ID = 1

# YOUTUBE
YOUTUBE_AUTH_EMAIL = 'coneptum@gmail.com'
YOUTUBE_AUTH_PASSWORD = 'tumconep2012'
YOUTUBE_DEVELOPER_KEY = 'AI39si6_Enu4odz-IDBXNjgciY68sYUG9Rvvw-tArLx9Z-RRbIVVTz69t7lilgW2XhxdmTFtRAH8nU6nq358_mFktq43RIuJPg'
YOUTUBE_CLIENT_ID = 'client-id'
YOUTUBE_UPLOAD_REDIRECT_URL = '/demo_gift/'

# EMAIL
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'coneptum@gmail.com'
EMAIL_HOST_PASSWORD = 'tumconep2012'
DEFAULT_FROM_EMAIL = 'coneptum@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = 'coneptum@gmail.com'
#from django.core.mail import send_mail
#send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)
