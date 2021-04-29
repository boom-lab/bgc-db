from django.contrib import admin
from import_export.admin import ExportMixin

# Register your models here.
from .models import *

class SensorTypesAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE', 'DESCRIPTION']
    list_per_page = 100


admin.site.register(sensor_types, SensorTypesAdmin)

class SensorMakersAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100


admin.site.register(sensor_makers, SensorMakersAdmin)

class SensorModelsAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100


admin.site.register(sensor_models, SensorModelsAdmin)


class InstrumentTypesAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100


admin.site.register(instrument_types, InstrumentTypesAdmin)


class PlatformMakersAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100


admin.site.register(platform_makers, PlatformMakersAdmin)


class PlatformTypesAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ['VALUE','DISPLAY','KEY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100


admin.site.register(platform_types, PlatformTypesAdmin)


class TransmissionSystemsAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ['VALUE','DISPLAY','ACTIVE','SOURCE','DESCRIPTION']
    list_per_page = 100


admin.site.register(transmission_systems, TransmissionSystemsAdmin)

class InstitutionsAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ['VALUE','DISPLAY','ACTIVE','DESCRIPTION']
    list_per_page = 100


admin.site.register(institutions, InstitutionsAdmin)

class FundersAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ['VALUE','DISPLAY','ACTIVE','DESCRIPTION']
    list_per_page = 100


admin.site.register(funders, FundersAdmin)

class EventsAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ['VALUE','DISPLAY','ACTIVE','DESCRIPTION']
    list_per_page = 100


admin.site.register(events, EventsAdmin)