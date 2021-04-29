from django.contrib import admin
from .models import cycle_metadata, continuous_profile, discrete_profile, park, mission_reported

# Register your models here.
class CycleMetadataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in cycle_metadata._meta.fields]
    list_display_links = None
    list_per_page = 25


admin.site.register(cycle_metadata, CycleMetadataAdmin)


class MissionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in mission_reported._meta.fields]
    list_display_links = None
    list_per_page = 25


admin.site.register(mission_reported, MissionAdmin)


class ContinuousProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in continuous_profile._meta.fields]
    list_display_links = None
    list_per_page = 25


admin.site.register(continuous_profile, ContinuousProfileAdmin)

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