
from django.contrib.auth.models import User 
from django.db.models import JSONField,IntegerField,CharField,ForeignKey,Model
from django.db.models import ManyToManyField,OneToOneField,CASCADE,DateField

from cartographer.services import getQuarter

class Country(Model):
    class Meta:
        verbose_name_plural = "countries"

    gwno = IntegerField(null = False,primary_key=True)
    name = CharField(max_length = 150, null = False)
    shape = JSONField(default = dict, null = False)
    #assignees = ManyToManyField(User,related_name="countries")

    def __str__(self):
        return f"{self.gwno} - {self.name}"

class Profile(Model):
    meta = JSONField(default = dict, null = True, blank = True)
    user = OneToOneField(User,on_delete=CASCADE, null=False)
    countries = ManyToManyField(Country,related_name="assignees")

    def __str__(self):
        return f"profile of {self.user.username}" # pylint: disable=no-member

class Shape(Model):
    author = ForeignKey(User,
       related_name = "Shapes",
       on_delete = CASCADE, null = False)

    country = ForeignKey(Country, 
            related_name = "Shapes", 
            on_delete = CASCADE, 
            null = False)

    shape =  JSONField(default = dict, null = False)
    year = IntegerField(null=False)
    quarter = IntegerField(null=False)

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
