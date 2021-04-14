from django.contrib import admin
from .models import profile_metadata, profile, park, mission_reported

# Register your models here.
class ProfileMetadataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in profile_metadata._meta.fields]
    list_display_links = None
    list_per_page = 25


admin.site.register(profile_metadata, ProfileMetadataAdmin)


class MissionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in mission_reported._meta.fields]
    list_display_links = None
    list_per_page = 25


admin.site.register(mission_reported, MissionAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('DEPLOYMENT','PROFILE_METADATA','MISSION', 'DATE_ADD', 'PRES','TEMP', 'PSAL', 'NCTD', 'OPH', 'OTV', 'NO', 'MCH1', 'MCH2', 
    'MCH3', 'NM', 'OCR1', 'OCR2', 'OCR3', 'OCR4', 'NI', 
        'IN', 'AZ', 'SA', 'CT', 'SIGMA0', 'Z', 'DOXY', 'CHLA', 'BBP700', 'CDOM', 'WN_IRR380', 'WN_IRR412', 'WN_IRR490', 'PAR')
    list_display_links = None
    list_per_page = 25


admin.site.register(profile, ProfileAdmin)


class ParkAdmin(admin.ModelAdmin):
    list_display = ('DEPLOYMENT','DATE_ADD', 'DATE_MEASURED', 'PRES','TEMP','PSAL', 'OPH', 'OTV')
    list_display_links = None
    list_per_page = 25


admin.site.register(park, ParkAdmin)