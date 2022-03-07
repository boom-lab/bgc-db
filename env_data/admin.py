from django.contrib import admin
from .models import cycle_metadata, continuous_profile, discrete_profile, park, mission_reported, nitrate_continuous_profile

# Register your models here.
class CycleMetadataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in cycle_metadata._meta.fields]
    list_per_page = 10
    list_filter = ['DEPLOYMENT__PLATFORM_TYPE']
    search_fields = ('DEPLOYMENT__FLOAT_SERIAL_NO','DEPLOYMENT__PLATFORM_NUMBER')


admin.site.register(cycle_metadata, CycleMetadataAdmin)


class MissionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in mission_reported._meta.fields]
    list_display_links = None
    list_per_page = 20
    list_filter = ['DEPLOYMENT__PLATFORM_TYPE']
    search_fields = ('DEPLOYMENT__FLOAT_SERIAL_NO','DEPLOYMENT__PLATFORM_NUMBER')


admin.site.register(mission_reported, MissionAdmin)


class ContinuousProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in continuous_profile._meta.fields]
    list_display_links = None
    list_per_page = 25


admin.site.register(continuous_profile, ContinuousProfileAdmin)

class NitrateContinuousProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in nitrate_continuous_profile._meta.fields]
    list_display_links = None
    list_per_page = 25


admin.site.register(nitrate_continuous_profile, NitrateContinuousProfileAdmin)

class DiscreteProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in discrete_profile._meta.fields]
    list_display_links = None
    list_per_page = 25


admin.site.register(discrete_profile, DiscreteProfileAdmin)


class ParkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in park._meta.fields]
    list_display_links = None
    list_per_page = 25


admin.site.register(park, ParkAdmin)