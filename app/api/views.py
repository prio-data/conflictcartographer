import json
from datetime import datetime
from collections import defaultdict

import pydantic

from django.http import HttpResponse,HttpRequest,JsonResponse
from django.shortcuts import render,redirect

from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib import auth
from django.views.decorators.http import require_http_methods

from rest_framework import viewsets, status, exceptions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions

from api import models, filters
from api.models import Country,ProjectDescription,WaiverText

from cartographer.services import currentQuarter,currentYear
from api.validation import CountryFeatureCollection
from api.forms import ProfileForm

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
    permission_classes = [permissions.IsAuthenticated]

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
    try:
        countries = Country.objects.all().filter(assignees__pk = request.user.profile.pk)
        return Response(CountryMetaSerializer(countries,many=True,context={"request":request}).data)
    except Exception as e:
        return Response([])

# ================================================
# Shape

def prepRequestData(request:HttpRequest):
    """
    Puts all "non-variable" data into a JSON field "values".
    Makes the schema really flexible.
    """
    NONVAR = ("year","shape","quarter","author","country","vizId")
    request.data["values"] = {k:v for k,v in request.data.items() if k not in NONVAR}
    return request

class ShapeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Shape
        fields = ["url","country","shape","values"]

class ShapeViewSet(viewsets.ModelViewSet):
    """
    Strict viewset that only allows users to:
    GET Shapes which they have authored
    POST Shapes to projects they are part of
    """

    queryset = models.Shape.objects.all()
    serializer_class = ShapeSerializer  

    filterset_fields = ["country"]

    permission_classes = [permissions.IsAuthenticated]

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
        prepRequestData(request)

        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save(author = self.request.user)
            return HttpResponse(serializer.data["url"], status=status.HTTP_201_CREATED)

        else:
            return HttpResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format = None):
        request = prepRequestData(request)

        shape = self.get_object(pk)
        shape.values = request.data["values"]
        shape.save()

        return HttpResponse(serializer.data["url"])

def whoami(request):
    return JsonResponse({"name": request.user.username, "waiver": request.user.profile.waiver})

def projectInfo(request:HttpRequest):
    verbose = request.GET.get("verbose","false") == "true"

    project = ProjectDescription.objects.filter(active=True).first()

    if project is None:
        data = {"status":"error",
                "title":"Missing",
                "description":"No project has been defined yet!"}
    else:
        description = project.long_description if verbose else project.description
        data = {"status":"ok",
                "title":project.title,
                "description":description}

    return JsonResponse(data)

def waiver(request:HttpRequest)->HttpResponse:
    if request.method == "GET":
        try:
            wt = WaiverText.objects.filter(active=True).first().content
        except Exception as e:
            wt = f"No waiver text defined! ({str(e)})"
        return JsonResponse({"status":"ok","message":wt})
    elif request.method=="POST":
        try:
            data = json.loads(request.body)
            agreed = data["agree"]
        except (json.decoder.JSONDecodeError,KeyError):
            return HttpResponse(status=400)
        if agreed:
            request.user.profile.waiver = True
            request.user.profile.save()
            return JsonResponse({"status":"ok","message":"Thanks"})
        else:
            return JsonResponse({"status":"ok","message":"Did not agree"})
    else:
        return HttpResponse(status=405)

@require_http_methods(["POST"])
def updateCountries(request):
    if not request.user.is_staff:
        return JsonResponse({"status":"error","messages":"permission denied"},status=status.HTTP_403_FORBIDDEN)

    class CountryDataUpload(pydantic.BaseModel):
        small: CountryFeatureCollection 
        large: CountryFeatureCollection
    try:
        uploaded = CountryDataUpload(**json.loads(request.body.decode()))
        getCountries = lambda fc: {c.properties.CNTRY_NAME for c in fc.features}
        assert len(uploaded.small.features) == len(uploaded.large.features)
        assert getCountries(uploaded.small) == getCountries(uploaded.large)
    except Exception as e:
        return JsonResponse({"status":"error","messages":str(e)},status=status.HTTP_400_BAD_REQUEST)

    saved = 0
    updated = 0

    for small,large in zip(uploaded.small.features,uploaded.large.features):
        try:
            c = Country.objects.get(gwno = small.properties.GWCODE)
        except Country.DoesNotExist:
            c = Country(
                    gwno = small.properties.GWCODE,
                    name = small.properties.CNTRY_NAME,
                    iso2c = small.properties.ISO1AL2,
                    shape = dict(large.geometry),
                    simpleshape = dict(small.geometry)
                )
            saved += 1
        else:
            c.iso2c = small.properties.ISO1AL2
            c.name = small.properties.CNTRY_NAME
            c.shape = dict(large.geometry)
            c.simpleshape = dict(small.geometry)
            updated += 1
        c.save()

    return JsonResponse({"status":"success","saved":saved,"updated":updated})

def editProfile(request:HttpRequest)->HttpResponse:
    if request.method == "GET":
        profile = request.user.profile
        form = ProfileForm(profile.meta)
        return render(request,"registration/editprofile.html",{"form":form})
    elif request.method =="POST":
        data = ProfileForm(request.POST)
        if data.is_valid():
            request.user.profile.meta = data.cleaned_data
            request.user.profile.save()
            return redirect("/")
    else:
        return HttpResponse(status=405)

def hasProfile(request:HttpRequest)->HttpResponse:
    return JsonResponse({"status":"ok","profile":bool(request.user.profile.meta)})
