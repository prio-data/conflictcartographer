from django.shortcuts import render
from django.http import HttpResponse 

from django.contrib.auth.models import User

from django_filters import rest_framework as filters

from rest_framework.viewsets import ModelViewSet 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from api.models import IntensityDrawnShape, CountryProject
from api.serializers import UserSerializer, IntensityDrawnShapeSerializer, CountryProjectSerializer, CountryProjectDetailSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ShapeViewSet(ModelViewSet):
    queryset = IntensityDrawnShape.objects.all()
    serializer_class = IntensityDrawnShapeSerializer
    filterset_fields = [
            "intensity",
            "confidence",
            "author",
            "project"]

    def create(self,request,*args,**kwargs):
        domany = isinstance(request.data, list)
        serializer = self.get_serializer(data = request.data, many = domany)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return HttpResponse(serializer.data["url"], status=status.HTTP_201_CREATED)

    def put(self, request, pk, format = None):
        layer = self.get_object(pk)
        serializer = self.get_serializer(data = request.data)
        print("doing something")
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data["url"])
        else:
            return HttpResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(ModelViewSet):
    queryset = CountryProject.objects.all()
    serializer_class = CountryProjectSerializer

class ProjectDetails(ModelViewSet):
    queryset = CountryProject.objects.all()
    serializer_class = CountryProjectDetailSerializer
