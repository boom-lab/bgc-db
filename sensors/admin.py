from django.contrib import admin
from .models import sensor
from .views import sensors_csv
from django.conf.urls import url
#from import_export import resources
from import_export.admin import ExportMixin

#If want to control what fields go into import-export
# class SensorResource(resources.ModelResource):
#     class Meta:
#         model=sensor
#         fields=[field.name for field in sensor._meta.fields]

class SensorAdmin(ExportMixin, admin.ModelAdmin):
    #resource_class = SensorResource

    all_fields = [field.name for field in sensor._meta.fields]

    list_display = all_fields
    list_display_links = None #('Record_Date',)
    search_fields = ('DEPLOYMENT',)
    list_per_page = 25
    list_filter = ('DEPLOYMENT',)

    #Add custom detail view to urls
    def get_urls(self):
        urls = super(SensorAdmin, self).get_urls()
        my_urls = [
            url(r'^sensor_export/$', self.admin_site.admin_view(sensors_csv), name='sensor_csv')
        ]
        return my_urls + urls


admin.site.register(sensor, SensorAdmin)
