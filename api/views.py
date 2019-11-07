from django.shortcuts import render
from django.http import HttpResponse 

from django.contrib.auth.models import User

from django_filters import rest_framework as filters

from rest_framework.viewsets import ModelViewSet 

from rest_framework import permissions
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes

# Local
from api.models import IntensityDrawnShape, CountryProject
from api.serializers import UserSerializer, IntensityDrawnShapeSerializer, CountryProjectSerializer, CountryProjectDetailSerializer, RegSerializer

from api.permissions import IsOwnerOrReadOnly

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
            IsOwnerOrReadOnly]
                            

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

@api_view(["POST"])
@permission_classes([permissions.IsAdminUser])
def create_auth(request):
    serialized = RegSerializer(data = request.data)
    if serialized.is_valid():
        User.objects.create_user(
                serialized.data["username"],
                serialized.data["email"],
                serialized.data["password"]
        )
        return HttpResponse(serialized.data, status = status.HTTP_201_CREATED)
    else:
        return HttpResponse(serialized._errors, status = status.HTTP_400_BAD_REQUEST)
