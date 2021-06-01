from django.contrib import admin
from .models import mission
from .views import export_NAVIS_mission_config
from import_export.admin import ExportMixin

def duplicate_record(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()

duplicate_record.short_description = "Duplicate selected missions"


def config_file(modeladmin, request, queryset):
    ids = []
    for record in queryset:
        ids.append(record.id)

    return export_NAVIS_mission_config(request, ids)


config_file.short_description = "Export Mission Config File"


class MissionAdmin(ExportMixin, admin.ModelAdmin):
    all_fields = [field.name for field in mission._meta.fields]

    list_display = all_fields
    #list_display_links = ('Record_Date',)
    search_fields = ('DEPLOYMENT',)
    list_per_page = 25
    list_filter = ('DEPLOYMENT',)
    actions = [duplicate_record, config_file]


admin.site.register(mission, MissionAdmin)
