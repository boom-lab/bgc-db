from django.contrib import admin
from import_export.admin import ExportMixin
import json
from .models import sensor
from django.urls import reverse
from django.utils.safestring import mark_safe 

class SensorAdmin(ExportMixin, admin.ModelAdmin):

    all_fields = [field.name for field in sensor._meta.fields]
    list_display = ['edit_link','qc_link','DEPLOYMENT','ADD_DATE','SENSOR','SENSOR_MAKER',
        'SENSOR_MODEL','SENSOR_SERIAL_NO','SENSOR_CALIB_DATE','PREDEPLOYMENT_CALIB_EQUATION',
        'PREDEPLOYMENT_CALIB_COEFFICIENT_short','COMMENTS']
    list_display_links = None
    search_fields = ('DEPLOYMENT__FLOAT_SERIAL_NO',)
    list_per_page = 25
    list_filter = ('SENSOR',)

    def PREDEPLOYMENT_CALIB_COEFFICIENT_short(self, obj):
        if obj.PREDEPLOYMENT_CALIB_COEFFICIENT:
            return json.dumps(obj.PREDEPLOYMENT_CALIB_COEFFICIENT)[0:28] + "..."
        return None
    PREDEPLOYMENT_CALIB_COEFFICIENT_short.short_description = "PREDEPLOYMENT_CALIB_COEFFICIENT"

    #Custom edit link
    def edit_link(self, obj):
        app = obj._meta.app_label
        model = obj._meta.model_name
        admin_url = reverse("admin:{}_{}_change".format(app, model),  args=(obj.pk,))

        return mark_safe('<a href="{}">Edit</a>'.format(
            admin_url
        ))
    edit_link.short_description = 'Edit'

    #Add mission link
    def qc_link(self, obj):
        admin_url = reverse("admin:sensor_qc_sensor_qc_add")

        return mark_safe('<a href="{}">Add QC</a>'.format(admin_url + "?SENSOR=" + str(obj.pk)))
    qc_link.short_description = 'Add QC Record'


admin.site.register(sensor, SensorAdmin)
