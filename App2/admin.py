from django.contrib import admin
from .models import Farm, Pest, Surveillance, EntryExitLog, Task

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'owner', 'total_plants', 'stocking_rate']
    list_filter = ['owner', 'created_at']
    search_fields = ['name', 'location']

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

@admin.register(EntryExitLog)
class EntryExitLogAdmin(admin.ModelAdmin):
    list_display = ['farm', 'company_name', 'person_name', 'purpose', 'date', 'time']
    list_filter = ['farm', 'date']
    search_fields = ['company_name', 'person_name', 'purpose', 'remarks']
    date_hierarchy = 'date'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['farm', 'title', 'task_type', 'scheduled_date', 'scheduled_time']
    list_filter = ['farm', 'task_type', 'scheduled_date']
    search_fields = ['title', 'description']