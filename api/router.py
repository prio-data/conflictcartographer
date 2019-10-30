from rest_framework import routers
from .views import UserViewSet,ShapeViewSet,CountryViewSet
from django.urls import include,path

router = routers.DefaultRouter()
router.register(r"users",UserViewSet)
router.register(r"shapes",ShapeViewSet)
router.register(r"countries",CountryViewSet)

