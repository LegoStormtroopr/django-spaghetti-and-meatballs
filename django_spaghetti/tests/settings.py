"""
Django settings for data_interrogator project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'just_another_test_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            [os.path.join(BASE_DIR, 'templates')]
        ],
        'APP_DIRS': True,
    },
]

TEMPLATE_DIRS = TEMPLATES[0]['DIRS']

INSTALLED_APPS = (
    'django_spaghetti.tests',
    'django_spaghetti',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
)

ROOT_URLCONF = 'django_spaghetti.tests.urls'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

SPAGHETTI_SAUCE = {
    'apps': ['tests', 'auth'],
    'exclude': {},
    'show_fields': False,
    'ignore_self_referential': True,
}
