
from django.contrib.auth.models import User 
from api.models import IntensityDrawnShape, CountryProject, Country
from rest_framework import serializers

class IntensityDrawnShapeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IntensityDrawnShape
        fields = ["url","project","author","date","geometry","intensity","confidence","pk"]

class CountryProjectSerializer(serializers.HyperlinkedModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
            queryset = User.objects.all(),
            many = True)

    class Meta:
        model = CountryProject
        fields = ["url","pk","name","lat","lon","zoom","participants"]

class CountryProjectDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CountryProject 
        fields = ["shape","lat","lon","zoom","pk"]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    projects = CountryProjectSerializer(many = True, read_only = True)

    class Meta:
        model = User
        fields = ["url","username","email","groups","pk","projects"]
