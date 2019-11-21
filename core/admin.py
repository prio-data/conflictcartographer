from django.contrib import admin
from core.models import Invitation, Cohort

# Register your models here.

@admin.register(Invitation)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Cohort)
class ProjectAdmin(admin.ModelAdmin):
    pass
