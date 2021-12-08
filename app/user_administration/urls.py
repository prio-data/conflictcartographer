
from django.contrib.urls import path
from user_administration.views import delete_me

urls = [
        path("/api/deleteme/",delete_me)
    ]
