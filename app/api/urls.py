
from django.urls import path, include
from rest_framework.urls import path
from rest_framework import routers

from api.views import ShapeViewSet, CountryViewSet, projects

router = routers.DefaultRouter()

router.register(r"shapes",ShapeViewSet)
router.register(r"countries",CountryViewSet)

urlpatterns = [
    # Pk is passed as a query, even though it is a path?
    # Magical!
    #path("api/profile/<int:pk>/", profile),
    path("api/assigned/", projects),
    path("api/",include(router.urls)),
]
