
from rest_framework import serializers
from api import models

# ================================================
# Auth

class UserSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
          model = models.User 
          fields = ["url","username","email","projects"]

# ================================================
# Project 

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Project
        fields = ["url","country","name","startdate","enddate","pk"]
     
class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Country
        fields = ["url","name","gwno","shape"]

# ================================================
# Shape 

class ShapeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Shape
        fields = ["url","project","author","shape","created","updated","intensity","confidence"]

