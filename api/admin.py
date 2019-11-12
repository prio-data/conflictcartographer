from django.contrib import admin
from api.models import Project, Shape, Country

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Shape)
class DrawnShapeAdmin(admin.ModelAdmin):
    pass

@admin.register(Country)
class DrawnShapeAdmin(admin.ModelAdmin):
    pass

