
from django.urls import path, include

from api.router import router
from api.views import profile 
from rest_framework.urls import path

urlpatterns = [
    # Pk is passed as a query, even though it is a path?
    # Magical!
    path("api/profile/<int:pk>/", profile),
    path("api/",include(router.urls)),
]
