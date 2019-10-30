from django.contrib import admin
from api.models import Country

# Register your models here.

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass

