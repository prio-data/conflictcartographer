
from collections import defaultdict

from django.http import HttpResponse

from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib import auth

from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api import serializers, models, permissions, util, filters
from datetime import datetime

import os
import json

# ================================================
# Utility viewsets

@api_view()
@permission_classes([permissions.permissions.IsAuthenticated])
def profile(request,pk):
    if not request.user.pk == int(pk) and not request.user.is_staff:
        raise exceptions.PermissionDenied
    q = auth.models.User.objects.filter(pk = int(pk))

    if len(q) > 0:
        user = q[0]
    else:
        raise exceptions.NotFound

    defaultdate = lambda y,m,d: datetime(y,m,d, tzinfo = timezone.get_current_timezone())
    mindate = lambda: defaultdate(1,1,1) 
    maxdate = lambda: defaultdate(9999,1,1) 

    workdone = defaultdict(int) 
    lastworked = defaultdict(mindate)
    firstworked = defaultdict(maxdate)

    def fixDefault(date):
        if (date == mindate()) | (date == maxdate()):
            return None
        else:
            return date 

    shapes = models.Shape.objects.filter(author = user)
    projects = models.Project.objects.filter(participants = user)
    projects = filters.active(projects, request)

    serialize = lambda p: serializers.ProjectSerializer(p, context = {"request":request})
    get_repr = lambda p: serialize(p).data

    projects = [get_repr(p) for p in projects]
    projects = {p["pk"]:p for p in projects}

    for s in shapes:
        workdone[s.project.pk] += 1
        lastworked[s.project.pk] = max(lastworked[s.project.pk], s.updated)
        firstworked[s.project.pk] = min(firstworked[s.project.pk], s.updated)

    projectKeys = [*projects.keys()] 
    for k in projectKeys:
        projects[k].update({
            "shapes": workdone[k],
            "first": fixDefault(firstworked[k]),
            "last": fixDefault(lastworked[k])
        })

    profile = {
        "name": user.username,
        "pk": user.pk,
        "projects": [*projects.values()],
    }
    return Response(profile)

# ================================================
# Auth
class UserViewSet(viewsets.ModelViewSet):

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer  

    permission_classes = [permissions.permissions.IsAdminUser]

# ================================================
# Project

class ProjectViewSet(viewsets.ModelViewSet):
    """
    This view is restrictive to non-admin users in that it only returns
    projects which the user is registered as a participant to. Also,
    non-admin users can only view projects that are currently active.
    """

    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer  

    filterset_fields = ["participants","startdate","enddate","country"]

    permission_classes = [permissions.permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This override restricts the returned data if the user is not admin.
        """

        now = datetime.now()

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        if not self.request.user.is_staff:
            queryset = queryset.filter(
                startdate__lt = now, 
                enddate__gt = now,
                participants = self.request.user
        )

        return queryset

class CountryViewSet(viewsets.ModelViewSet):

    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer  

    #filterset_fields = [
    #]

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

    filterset_fields = ["project"]

    # Latter permissions only apply to POST requests.
    permission_classes = [permissions.permissions.IsAuthenticated]
    user_permissions = [permissions.IsOnProject, permissions.ProjectIsActive]
                          

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
