from django.contrib import admin
from import_export.admin import ExportMixin
from .models import file_processing, deployment_tracking

def set_skip(modeladmin, request, queryset):
    queryset.update(STATUS='Skip')

def set_fail(modeladmin, request, queryset):
    queryset.update(STATUS='Fail')

def set_reprocess(modeladmin, request, queryset):
    queryset.update(STATUS='Reprocess')

class FileProcessingAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['DIRECTORY','FLOAT_SERIAL_NO','CYCLE','STATUS','DETAILS','DATE', ]
    #list_display_links = ('Record_Date',)
    search_fields = ('STATUS','FLOAT_SERIAL_NO')
    list_per_page = 25
    list_filter = ('STATUS','FLOAT_SERIAL_NO')
    actions = [set_skip, set_fail, set_reprocess]


admin.site.register(file_processing, FileProcessingAdmin)

class DeploymentTrackingAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['DEPLOYMENT','EVENT','DATE','LOCATION','COMMENT','USER']
    #list_display_links = ('Record_Date',)
    search_fields = ('DEPLOYMENT__FLOAT_SERIAL_NO',)
    list_per_page = 25
    list_filter = ('EVENT',)

    exclude = ['USER',]

    def save_model(self, request, obj, form, change):
        obj.USER = request.user
        super().save_model(request, obj, form, change)


admin.site.register(deployment_tracking, DeploymentTrackingAdmin)
