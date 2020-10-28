from .base import * 
import os

# ================================================
# Dev settings ===================================
# ================================================

SECRET_KEY = 'fgsfds'
DEBUG = True

# ?# ? # ? # ? # ? # ? # ? # ?  
ALLOWED_HOSTS = ["*"]

"""
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "js/",
        "STATS_FILE": os.path.join(FRONTEND_DIR,"webpack-stats.json"),
    }
}
"""

# ================================================
# ================================================
# DB 

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        "HOST":"0.0.0.0",
        "PORT":"5432",
        "USER":"conflictcartographer",
        "PASSWORD":"letmein",
        'NAME': "cc",
        "CONN_MAX_AGE": 3600 
    }
}

# ================================================
# ================================================
# PASSWORDS

AUTH_PASSWORD_VALIDATORS = [
]

EMAIL_HOST = "localhost"
EMAIL_HOST_USER = "testing@testing.test"
EMAIL_FROM_ADDRESS = "testing@testing.test"
EMAIL_PORT = 1202

INVITATION_LINK_BASE = "localhost:8000/accounts/ref/{key}/"
