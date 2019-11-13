
from api.views import whoami
from django.urls import path 

urlpatterns = [
    path("api/whoami/", whoami)
]
