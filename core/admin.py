from django.contrib import admin
from core.models import Invitation

# Register your models here.

@admin.register(Invitation)
class ProjectAdmin(admin.ModelAdmin):
    pass
