
from django.contrib.auth.models import User 
from api.models import IntensityDrawnShape, Country
from rest_framework import serializers

class IntensityDrawnShapeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IntensityDrawnShape
        fields = ["author","date","geometry","intensity","confidence","pk"]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url","username","email","groups","pk"]

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country 
        fields = ["name","lat","lon","zoom"]

