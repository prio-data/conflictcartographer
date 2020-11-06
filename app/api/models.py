
from django.contrib.auth.models import User 
from django.db.models import JSONField,IntegerField,CharField,ForeignKey,Model,BooleanField
from django.db.models import ManyToManyField,OneToOneField,CASCADE,DateField,TextField

from cartographer.services import getQuarter

from utils.mixins import OnlyOneActive

class Country(Model):
    class Meta:
        verbose_name_plural = "countries"

    gwno = IntegerField(null = False,primary_key=True)
    name = CharField(max_length = 150, null = False)
    iso2c = CharField(max_length=2,null = True)

    shape = JSONField(null = False)
    simpleshape = JSONField(null=False)

    def __str__(self):
        return f"{self.gwno} - {self.name}"

class Profile(Model):
    meta = JSONField(default = dict, null = True, blank = True)
    user = OneToOneField(User,on_delete=CASCADE)
    countries = ManyToManyField(Country,related_name="assignees")

    def __str__(self):
        return f"profile of {self.user.username}" # pylint: disable=no-member

class ProjectDescription(OnlyOneActive,Model):
    title = CharField(max_length = 128)
    description = TextField()
    long_description = TextField()

    def __str__(self):
        return "Project description"

class Shape(Model):
    author = ForeignKey(User,
       related_name = "Shapes",
       on_delete = CASCADE, null = False)

    country = ForeignKey(Country, 
            related_name = "Shapes", 
            on_delete = CASCADE, 
            null = False)

    shape =  JSONField(default = dict, null = False)

    date = DateField(auto_now_add=True)

    values = JSONField(default = dict)

    @property
    def quarter(self):
        return getQuarter(self.date)

    @property
    def year(self):
        return self.date.year

    def __str__(self):
        return f"Shape {self.quarter}/{self.year}@{self.country.name}"
