"""
Django settings for django-spaghetti test project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'just_another_test_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
    },
]

INSTALLED_APPS = (
    'django_spaghetti.tests',
    'django_spaghetti',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
)

ROOT_URLCONF = 'django_spaghetti.tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'

SPAGHETTI_SAUCE = {
    'apps': ['tests', 'auth'],
    'exclude': {},
    'show_fields': False,
    'ignore_self_referential': True,
}
