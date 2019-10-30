from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.

class Shape(models.Model):
    geometry = JSONField("geoJSON")

class DrawnShape(Shape):
    author = models.ForeignKey("auth.User", 
            related_name = "shapes",
            on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now = True)
    def __str__(self):

        daterepr = datetime.strftime(self.date,"%d/%m/%Y")
        return Super(self).__str__ + f" drawn on {daterepr} by {author}"

class IntensityDrawnShape(DrawnShape):
    intensity = models.IntegerField("Expected intensity")
    confidence = models.IntegerField("Confidence in prediction")
    def __str__(self):
        return Super(self).__str__ + " with intensity {self.intensity} and confidence {self.confidence}"

class Country(models.Model):
    name = models.CharField(max_length = 150)
    lat = models.FloatField("Latitude of centroid")
    lon = models.FloatField("Longitude of centroid")
    zoom = models.FloatField("Zoom level")

    def __str__(self):
        return f"{self.name}: lat {self.lat}|lon {self.lon}|zoom {self.zoom}"

