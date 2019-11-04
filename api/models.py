from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime


# Base classes ===================================

class Shape(models.Model):
    geometry = JSONField("geoJSON")

class Country(models.Model):
    name = models.CharField(max_length = 150)
    #lat = models.FloatField("Latitude of centroid")
    #lon = models.FloatField("Longitude of centroid")
    #zoom = models.FloatField("Zoom level")
    shape = JSONField("geoJSON",default = dict)

# Models =========================================

class CountryProject(Country):
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    participants = models.ManyToManyField("auth.User", related_name="projects", blank = True) 
    importance = models.PositiveIntegerField(default = 5,
            validators = [MinValueValidator(1), MaxValueValidator(10)])
    def __str__(self):
        return f"{self.name}"

class DrawnShape(Shape):

    author = models.ForeignKey("auth.User", 
            related_name = "shapes",
            on_delete = models.CASCADE)

    project = models.ForeignKey(CountryProject,
            related_name = "shapes",
            on_delete = models.CASCADE)

    date = models.DateTimeField(auto_now = True)

class IntensityDrawnShape(DrawnShape):

    intensity = models.IntegerField("Expected intensity")
    confidence = models.IntegerField("Confidence in prediction")
    def __str__(self):
        return f"{self.author.username} @ {self.project.name} {datetime.strftime(self.date,'%d/%m/%Y')}"

    class Meta:
        verbose_name = "Drawn shape"
        verbose_name_plural = "Drawn shapes"
