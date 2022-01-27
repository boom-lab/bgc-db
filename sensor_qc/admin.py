from django.contrib import admin
from import_export.admin import ExportMixin
from .models import sensor_qc

class SensorQCAdmin(ExportMixin, admin.ModelAdmin):

    all_fields = [field.name for field in sensor_qc._meta.fields]
    list_display = ["SENSOR","ADD_DATE","START_CYCLE","END_CYCLE","QC_LEVEL","PROBLEM"]
    list_display_links = ("SENSOR",)
    #search_fields = ("SENSOR",)
    list_per_page = 25
    #list_filter = ('SENSOR',)

admin.site.register(sensor_qc, SensorQCAdmin)
