from .base import * 
import os

# ================================================
# Dev settings ===================================
# ================================================

SECRET_KEY = 'fgsfds'
DEBUG = True

# ?# ? # ? # ? # ? # ? # ? # ?  
ALLOWED_HOSTS = ["*"]

# ================================================
# ================================================
# STATIC 

STATIC_ROOT = ""
STATIC_URL = '/frontend/dist/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "frontend/dist/"),
    os.path.join(BASE_DIR, "static"),
)

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "js/",
        "STATS_FILE": os.path.join(FRONTEND_DIR,"webpack-stats.json"),
    }
}

# ================================================
# ================================================
# DB 

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        "HOST":"0.0.0.0",
        "PORT":"2345",
        "USER":"postgres",
        "PASSWORD":"letmein",
        'NAME': "conflictcartographer" 
    }
}

# ================================================
# ================================================
# PASSWORDS

AUTH_PASSWORD_VALIDATORS = [
]
