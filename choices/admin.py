from django.contrib import admin
from import_export.admin import ExportMixin, ImportExportMixin

from choices import models as cm

class SensorTypesAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE', 'DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.sensor_types, SensorTypesAdmin)

class SensorMakersAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.sensor_makers, SensorMakersAdmin)

class SensorModelsAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.sensor_models, SensorModelsAdmin)


class PlatformMakersAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.platform_makers, PlatformMakersAdmin)


class PlatformTypesAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','KEY','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.platform_types, PlatformTypesAdmin)

class PlatformTypesAOMLAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.platform_types_aoml, PlatformTypesAOMLAdmin)

class PlatformTypesWMOAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.platform_types_wmo, PlatformTypesWMOAdmin)


class TransmissionSystemsAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.transmission_systems, TransmissionSystemsAdmin)


class InstitutionsAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.institutions, InstitutionsAdmin)

class FundersAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.funders, FundersAdmin)

class EventsAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.events, EventsAdmin)

class WMOrecorderTypesAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.wmo_recorder_types, WMOrecorderTypesAdmin)

class BatteryTypesAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE']
    list_per_page = 100
admin.site.register(cm.battery_types, BatteryTypesAdmin)

class BatteryManufacturersAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE']
    list_per_page = 100
admin.site.register(cm.battery_manufacturers, BatteryManufacturersAdmin)

class OriginCountriesAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE']
    list_per_page = 100
admin.site.register(cm.origin_countries, OriginCountriesAdmin)

class DeploymentPlatformAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','ACTIVE','TYPE','ICES','SOURCE','DESCRIPTION']
    list_per_page = 100
    search_fields = ('VALUE',)
admin.site.register(cm.deployment_platforms, DeploymentPlatformAdmin)

class TrackingErrorTypesAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.tracking_error_types, TrackingErrorTypesAdmin)