
from django.urls import path, include
from rest_framework.urls import path
from rest_framework import routers

from api.views import ShapeViewSet, CountryViewSet, projects, updateCountries,whoami,projectInfo,waiver

router = routers.DefaultRouter()

router.register(r"shapes",ShapeViewSet)
router.register(r"countries",CountryViewSet)

urlpatterns = [
    path("api/assigned/", projects),
    path("api/",include(router.urls)),
    path("api/updatecountries/",updateCountries,name="updatecountries"),
    path("api/whoami/",whoami),
    path("api/currentproject/",projectInfo),
    path("api/waiver/",waiver)
]
