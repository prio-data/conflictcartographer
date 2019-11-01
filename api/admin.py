from django.contrib import admin
from api.models import CountryProject, IntensityDrawnShape

# Register your models here.

@admin.register(CountryProject)
class CountryProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(IntensityDrawnShape)
class DrawnShapeAdmin(admin.ModelAdmin):
    pass

