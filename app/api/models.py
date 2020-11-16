from datetime import date 

from django.contrib.auth.models import User 
from django.db.models import JSONField,IntegerField,CharField,ForeignKey,Model,BooleanField
from django.db.models import ManyToManyField,OneToOneField,CASCADE,DateField,TextField

from annoying.fields import AutoOneToOneField

from cartographer.services import getQuarter,quarterRange

from utils.mixins import OnlyOneActive

class WaiverText(OnlyOneActive,Model):
    content = TextField(default="ENTER A WAIVER TEXT HERE",null=False)
    def __str__(self):
        return self.content[:50]+"..."


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
    user = AutoOneToOneField(User,on_delete=CASCADE)
    countries = ManyToManyField(Country,related_name="assignees")

    waiver = BooleanField(default = False)

    def __str__(self):
        return f"profile of {self.user.username}" # pylint: disable=no-member

class ProjectDescription(OnlyOneActive,Model):
    title = CharField(max_length = 128)
    description = TextField()
    long_description = TextField()

    def __str__(self):
        return "Project description"

class Answer(Model):
    class Meta:
        abstract = True

    date = DateField(null=False)
    author = ForeignKey(User,on_delete=CASCADE,null=False)
    country = ForeignKey(Country,on_delete=CASCADE,null=False)

    @property
    def quarter(self):
        return getQuarter(self.date)

    @property
    def year(self):
        return self.date.year

    def save(self,*args,**kwargs):
        if self.pk is None and self.date is None:
            print(today())
            self.date = today() 
        super().save(*args,**kwargs)

class Shape(Answer):
    #Name collision
    country = ForeignKey(Country,related_name="Shapes",on_delete=CASCADE,null=False)

    shape =  JSONField(default = dict, null = False)
    values = JSONField(default = dict)
    def __str__(self):
        return f"Shape {self.quarter}/{self.year}@{self.country.name}"

    def save(self,*args,**kwargs):
        s,e = quarterRange(self.date)
        nas = NonAnswer.objects.filter(
                author=self.author,
                country=self.country,
                date__gte=s,
                date__lte=e
                )

        if nas:
            nas.delete()

        super().save(*args,**kwargs)

class NonAnswer(Answer):
    def __str__(self):
        return f"Nonanswer {self.quarter}/{self.year}@{self.country.name}"
