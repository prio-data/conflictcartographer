
from collections import defaultdict

from django.http import HttpResponse,HttpRequest

from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib import auth

from rest_framework import viewsets, status, exceptions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions

from api import models, filters
from api.models import Country
from datetime import datetime

from cartographer.services import currentQuarter,currentYear

# ================================================
# Countries 
     
class CountryMetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Country
        fields = ["url","name","gwno"]

class CountryShapeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Country
        fields = ["url","shape"]

class CountryViewSet(viewsets.ModelViewSet):
    """
    Yields shape in detail view.
    """
    queryset = models.Country.objects.all()
    serializer_class = CountryMetaSerializer  
    permission_classes = [permissions.permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CountryShapeSerializer
        else:
            return CountryMetaSerializer

@api_view(("GET",))
def projects(request:HttpRequest)->HttpResponse:
    """
    Get list of countries assigned to current user.
    """
    countries = Country.objects.all().filter(assignees__pk = request.user.profile.pk)
    return Response(CountryMetaSerializer(countries,many=True,context={"request":request}).data)

# ================================================
# Shape

def prepRequestData(request:HttpRequest):
    NONVAR = ("year","shape","quarter","author","country","vizId")

    request.data["year"] = currentYear()
    request.data["quarter"] = currentQuarter()
    request.data["values"] = {k:v for k,v in request.data.items() if k not in NONVAR}

class ShapeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Shape
        fields = ["url","country","shape","year","quarter","values"]

class ShapeViewSet(viewsets.ModelViewSet):
    """
    Strict viewset that only allows users to:
    GET Shapes which they have authored
    POST Shapes to projects they are part of
    """

    queryset = models.Shape.objects.all()
    serializer_class = ShapeSerializer  

    filterset_fields = ["country"]

    # Latter permissions only apply to POST requests.
    permission_classes = [permissions.permissions.IsAuthenticated]

    #user_permissions = [permissions.IsOnProject, permissions.ProjectIsActive]

    def get_queryset(self):
        """
        This override restricts the returned data if the user is not admin.
        """

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        if not self.request.user.is_staff:
            queryset = queryset.filter(author = self.request.user)

        return queryset

    def create(self,request,*args,**kwargs):

        if not request.user.is_staff:
            permitted = True
            for p in self.user_permissions:
                permitted &= p().has_permission(request, self)
            if not permitted:
                raise exceptions.PermissionDenied
        
        prepRequestData(request)

        domany = isinstance(request.data, list)
        serializer = self.get_serializer(data = request.data, many = domany)

        if serializer.is_valid():
            serializer.save(author = self.request.user)
            return HttpResponse(serializer.data["url"], status=status.HTTP_201_CREATED)

        else:
            return HttpResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format = None):
        shape.values = request.data["values"]
        shape = self.get_object(pk)
        shape.save()
        return HttpResponse(serializer.data["url"])
