"""
Django settings for conflictcartographer project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os


# ================================================
# ================================================
# PATHS 

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# ================================================
# ================================================
# AUTH 

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

SITE_ID = 1

# ================================================
# ================================================
# APP 

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    "rest_framework",
    "core",
    #"invitations", # Maybe deprecated
    "django_filters",
    "webpack_loader",
    "livereload",
    "cartographer",
    "api",
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
    "livereload.middleware.LiveReloadScript",
]

ROOT_URLCONF = 'conflictcartographer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conflictcartographer.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ================================================
# ================================================
# REST framework 

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

# ================================================
# ================================================
# EMAIL STUFF 

EMAIL_INTERVAL = 1

PLAINTEXT_MAIL_TEMPLATE = "mail/invitation.txt"
HTML_MAIL_TEMPLATE = "mail/invitation.html"

# ================================================
# ================================================
# APP 

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    "formatters": {
        "standard":{
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,"logs/app.log"),
            "maxBytes": 1024*1024*5, # 5 MiB
            "backupCount": 5,
            "formatter": "standard",
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,"logs/app.request.log"),
            "maxBytes": 1024*1024*5, # 5 MiB
            "backupCount": 5,
            "formatter": "standard",
        },
    },
    'loggers': {
        '': {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ================================================
# ================================================
# STATIC 

STATIC_ROOT = os.path.join(BASE_DIR,"collect")
STATIC_URL = '/static/'
STATICFILES_DIRS = [
        os.path.join(BASE_DIR,"static")
        ]
