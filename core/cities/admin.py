from django.contrib import admin
from cities.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['title']
