
from collections import defaultdict

from django.http import HttpResponse

from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib import auth

from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api import serializers, models, permissions, filters
from datetime import datetime

# ================================================
# Utility viewsets

@api_view()
@permission_classes([permissions.permissions.IsAuthenticated])
def profile(request,pk):
    """
    Returns a user-profile, which is used to determine:
    * Which projects to show
    * What PK to use when posting shapes
    * Which username to show
    """
    if not request.user.pk == int(pk) and not request.user.is_staff:
        raise exceptions.PermissionDenied
    q = auth.models.User.objects.filter(pk = int(pk))

    if len(q) > 0:
        user = q[0]
    else:
        raise exceptions.NotFound

    shapes = models.Shape.objects.filter(author = user)
    countries = models.Country.objects.filter(assignees = user)

    serialize = lambda p: serializers.ProjectSerializer(p, context = {"request":request})
    get_repr = lambda p: serialize(p).data

    profile = {
        "name": user.username,
        "pk": user.pk,
        "countries": [c.gwno for c in countries]
    }

    return Response(profile)

# ================================================
# Countries 

class CountryViewSet(viewsets.ModelViewSet):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer  
    permission_classes = [permissions.permissions.IsAuthenticated]

# ================================================
# Shape

class ShapeViewSet(viewsets.ModelViewSet):
    """
    Strict viewset that only allows users to:
    GET Shapes which they have authored
    POST Shapes to projects they are part of
    """
    queryset = models.Shape.objects.all()
    serializer_class = serializers.ShapeSerializer  

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
        
        domany = isinstance(request.data, list)
        serializer = self.get_serializer(data = request.data, many = domany)

        if serializer.is_valid():
            serializer.save(author = self.request.user)
            return HttpResponse(serializer.data["url"], status=status.HTTP_201_CREATED)

        else:
            return HttpResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format = None):
        shape = self.get_object(pk)
        serializer = serializers.ShapeSerializer(shape,data = request.data)

        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data["url"])
        else:
            return HttpResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
