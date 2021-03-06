"""
For more information, please refer to the official documentation of the Django Project.
"""

SECRET_KEY = 'VerySecureSecretKey'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'codeflix',  # If you change this setting, be careful during the install.
        'USER': 'codeflix',  # If you change this setting, be careful during the install.
        'PASSWORD': 'VerySecretPassword',
        'HOST': 'localhost',  # If you change this setting, be careful during the install.
        'PORT': '5432',  # If you change this setting, be careful during the install.
    }
}

ALLOWED_HOSTS = []  # The list of domain names that Django is allowed to serve.

STATIC_ROOT = None  # The absolute path to the directory of the static files.

DEFAULT_FROM_EMAIL = "webmaster@localhost"
EMAIL_HOST = "localhost"

SITE_NAME = None
