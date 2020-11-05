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
# ================================================
# DYNAMIC CONFIG
# These settings are overridden by env variables,
# and typically vary between dev. and prod. 
# settings.
# ================================================
# ================================================
# ================================================


SECRET_KEY = os.getenv("SECRET_KEY","fgsfds")
DEBUG = False if os.getenv("PRODUCTION") else True 

DATABASES = {
        "default":{
            "ENGINE":"django.db.backends.postgresql_psycopg2",
            "HOST":os.getenv("DB_HOST","0.0.0.0"),
            "PORT":os.getenv("DB_PORT","5432"),
            "USER":os.getenv("DB_USER","conflictcartographer"),
            "PASSWORD":os.getenv("DB_PASSWORD","letmein"),
            "NAME":os.getenv("DB_NAME","cc"),
            "CONN_MAX_AGE": 3600
        }
}

if os.getenv("DB_SSL"):
    DATABASES["default"].update({
        "OPTIONS":{
            "sslmode":"verify-full",
            "sslrootcert":os.getenv("DB_SSL_CERT","/cert/BaltimoreCyberTrustRoot.crt.pem")
            }
        })

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # ???


EMAIL_HOST = os.getenv("EMAIL_HOST") 
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD") 
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER") 
EMAIL_FROM_ADDRESS = os.getenv("EMAIL_SENDER") 
EMAIL_PORT = int(os.getenv("EMAIL_PORT",0)) 
EMAIL_USE_TLS = False if os.getenv("EMAIL_NO_TLS") else True


# ================================================
# ================================================
# ================================================
# STATIC CONFIG
# These settings do not change between dev. 
# and prod.
# ================================================
# ================================================
# ================================================

ALLOWED_HOSTS = ["*"]

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
    "rest_framework",
    "invitations",
    "django_filters",
    "webpack_loader",
    #"livereload",
    "cartographer",
    "api",
    #"adminext",
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
    #"livereload.middleware.LiveReloadScript",
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

EMAIL_FROM = "noreply@prio.org"

EMAIL_INTERVAL = 1

DEFAULT_EMAIL_TITLE = "Invitation to participate in an expert survey"
DEFAULT_PLAINTEXT_MAIL_TEMPLATE = "mail/invitation.txt"
DEFAULT_HTML_MAIL_TEMPLATE = "mail/invitation.html"

PUBLIC_URL = "https://conflictcartographer.prio.org"
INVITATION_LINK_BASE = os.path.join(PUBLIC_URL,"accounts","ref")

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

# ================================================
# ================================================
# STATIC 

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR,"static")
STATIC_HOST = 'http://0.0.0.0:1337' if DEBUG else ''
STATIC_URL = STATIC_HOST + "/static/" 

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"compiled")
    ]

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
