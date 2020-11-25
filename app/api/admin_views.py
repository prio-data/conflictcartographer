
from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
#from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.routers import DefaultRouter

from django_filters import rest_framework as filters

from api.models import Shape,Feedback,Country


class AdminModelViewSet(ModelViewSet):
    permission_classes=[IsAdminUser]

class UserSerializer(ModelSerializer):
    class Meta:
        model = User 
        fields = ["username"]

class UserViewSet(AdminModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 

class ShapeFilter(filters.FilterSet):
    after = filters.DateFilter(field_name="date",lookup_expr="gte")
    before = filters.DateFilter(field_name="date",lookup_expr="lte")
    author = filters.ModelChoiceFilter(field_name="author",queryset=User.objects.all())
    gwno = filters.ModelChoiceFilter(field_name="country",queryset=Country.objects.all())


class ShapeSerializer(ModelSerializer):
    class Meta:
        model = Shape
        fields = ["country","shape","date","author","values"]

class ShapeViewSet(AdminModelViewSet):
    queryset = Shape.objects.all()
    serializer_class = ShapeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ShapeFilter

class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ["gwno","name","active"]

class CountryViewset(AdminModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer 
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ["active"] 

router = DefaultRouter()
router.register(r"shapes",ShapeViewSet,basename="adminshape")
router.register(r"users",UserViewSet,basename="user")
router.register(r"countries",CountryViewset,basename="admincountry")
