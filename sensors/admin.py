from django.contrib import admin
from import_export.admin import ExportMixin
import json
from .models import sensor

class SensorAdmin(ExportMixin, admin.ModelAdmin):

    all_fields = [field.name for field in sensor._meta.fields]

    list_display = ["id","DEPLOYMENT","ADD_DATE","SENSOR","SENSOR_MAKER","SENSOR_MODEL","SENSOR_SERIAL_NO","SENSOR_CALIB_DATE",
        "PREDEPLOYMENT_CALIB_EQUATION","PREDEPLOYMENT_CALIB_COEFFICIENT_short", "COMMENTS"]
    list_display_links = ('id',)
    search_fields = ('DEPLOYMENT__FLOAT_SERIAL_NO',)
    list_per_page = 25
    list_filter = ('SENSOR',)

    def PREDEPLOYMENT_CALIB_COEFFICIENT_short(self, obj):
        if obj.PREDEPLOYMENT_CALIB_COEFFICIENT:
            return json.dumps(obj.PREDEPLOYMENT_CALIB_COEFFICIENT)[0:28] + "..."
        return None
    PREDEPLOYMENT_CALIB_COEFFICIENT_short.short_description = "PREDEPLOYMENT_CALIB_COEFFICIENT"


admin.site.register(sensor, SensorAdmin)
