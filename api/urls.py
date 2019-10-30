from rest_framework import routers
from .views import UserViewSet,CountryViewSet
from django.urls import include,path

router = routers.DefaultRouter()
router.register(r"users",UserViewSet)
router.register(r"users",CountryViewSet)

