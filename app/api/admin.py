from django.contrib import admin
from api.models import Shape, Country,ProjectDescription

# Register your models here.

"""
@admin.register(Shape)
class DrawnShapeAdmin(admin.ModelAdmin):
    pass

@admin.register(Country)
class DrawnShapeAdmin(admin.ModelAdmin):
    pass
"""

@admin.register(ProjectDescription)
class ProjectAdmin(admin.ModelAdmin):
    list_display=("title","active")
