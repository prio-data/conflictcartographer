from rest_framework import routers
from .views import ShapeViewSet,CountryViewSet

router = routers.DefaultRouter()

router.register(r"shapes",ShapeViewSet)
router.register(r"countries",CountryViewSet)
