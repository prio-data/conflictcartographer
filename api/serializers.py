
from django.contrib.auth.models import User 
from api.models import IntensityDrawnShape, CountryProject, Country
from rest_framework import serializers

class IntensityDrawnShapeSerializer(serializers.HyperlinkedModelSerializer):
    #author = serializers.ReadOnlyField(source = "author.username")
    #project = serializers.ReadOnlyField(source = "project.name")
    class Meta:
        model = IntensityDrawnShape
        fields = ["url","project","author","date","geometry","intensity","confidence",]

class CountryProjectSerializer(serializers.HyperlinkedModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
            queryset = User.objects.all(),
            many = True)

    class Meta:
        model = CountryProject
        fields = ["url","pk","name","participants"]

class CountryProjectDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CountryProject 
        fields = ["shape","pk"]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    projects = CountryProjectSerializer(many = True, read_only = True)

    class Meta:
        model = User
        fields = ["url","username","email","groups","projects"]

class RegSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username","email","password"]
