from django.contrib import admin
from import_export.admin import ExportMixin

from .models import sensor

class SensorAdmin(ExportMixin, admin.ModelAdmin):

    all_fields = [field.name for field in sensor._meta.fields]

    list_display = all_fields
    list_display_links = ('id',)
    search_fields = ('DEPLOYMENT',)
    list_per_page = 25
    list_filter = ('DEPLOYMENT',)


admin.site.register(sensor, SensorAdmin)
