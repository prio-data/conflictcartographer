
from django.db import models

from django.core import validators

from django.contrib import auth
from django.contrib.postgres import fields 

from datetime import datetime

# ================================================
# Util


# ================================================
# Auth

User = auth.models.User

# ================================================
# Project

class Project(models.Model):
    name = models.CharField(max_length = 150)

    participants = models.ManyToManyField(User,
        related_name = "projects")

    country = models.ForeignKey("Country",
       related_name = "Projects",
       on_delete = models.CASCADE)

    startdate = models.DateTimeField()
    enddate = models.DateTimeField()

    def __str__(self):
        fixdate = lambda x: datetime.strftime(x, format = "%d/%m/%Y")
        return f"{self.pk} {self.name} ({self.country.name}) [{fixdate(self.startdate)} - {fixdate(self.enddate)}]: {len(self.participants.all())} participant(s)"

class Country(models.Model):
    name = models.CharField(max_length = 150) 
    gwno = models.IntegerField(default = -1) #TODO restrict?

    shape = fields.JSONField(default = dict) #GEOJSON
    capital_lat = models.IntegerField(default = 0)
    capital_lon = models.IntegerField(default = 0)

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return f"{self.gwno}-{self.name}"

# ================================================
# Shape

class Shape(models.Model):
    author = models.ForeignKey(User,
       related_name = "Shapes",
       on_delete = models.CASCADE, default = None)
    project = models.ForeignKey("Project",
        related_name = "Shapes",
        on_delete = models.CASCADE, default = None)

    shape =  fields.JSONField(default = dict) #GEOJSON
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    intensity = models.IntegerField(default = 0) #TODO make more flexible?
    confidence = models.IntegerField(default = 0)

    def __str__(self):
        timestamp = lambda x: datetime.strftime(x, format = "%d/%m/%Y %H:%M:%S")
        return f"{self.author.username}, {timestamp(self.created)} ({self.project.pk})"
