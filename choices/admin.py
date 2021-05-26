from django.contrib import admin
from import_export.admin import ExportMixin

# Register your models here.
from .models import *
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


class InstrumentTypesAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.instrument_types, InstrumentTypesAdmin)


class PlatformMakersAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.platform_makers, PlatformMakersAdmin)


class PlatformTypesAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','KEY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.platform_types, PlatformTypesAdmin)


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

class InstTypesAOMLAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.instrument_types_AOML, InstTypesAOMLAdmin)

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

class DeploymentPlatformAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['VALUE','DISPLAY','ACTIVE','TYPE','NODC','SOURCE','DESCRIPTION']
    list_per_page = 100
admin.site.register(cm.deployment_platforms, DeploymentPlatformAdmin)