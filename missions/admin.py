from django.contrib import admin
from .models import mission
from import_export.admin import ExportMixin

def duplicate_record(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
duplicate_record.short_description = "Duplicate selected missions"


class MissionAdmin(ExportMixin, admin.ModelAdmin):
    all_fields = [field.name for field in mission._meta.fields]

    list_display = all_fields
    #list_display_links = ('Record_Date',)
    search_fields = ('DEPLOYMENT',)
    list_per_page = 25
    list_filter = ('DEPLOYMENT',)
    actions = [duplicate_record]


admin.site.register(mission, MissionAdmin)
