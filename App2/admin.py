from django.contrib import admin
from .models import Farm, Pest, PlantLocation, Surveillance

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'owner', 'total_plants', 'stocking_rate']
    list_filter = ['owner', 'created_at']
    search_fields = ['name', 'location']

@admin.register(PlantLocation)
class PlantLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'farm', 'number_of_plants']
    list_filter = ['farm']
    search_fields = ['name', 'farm__name']

@admin.register(Pest)
class PestAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'reference_pest_id']
    list_filter = ['created_by']
    search_fields = ['name', 'description']

@admin.register(Surveillance)
class SurveillanceAdmin(admin.ModelAdmin):
    list_display = ['farm', 'pest', 'date_observed', 'severity', 'created_by']
    list_filter = ['severity', 'plant_part', 'date_observed', 'farm']
    search_fields = ['farm__name', 'pest__name', 'notes']
    date_hierarchy = 'date_observed'