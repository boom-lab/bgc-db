from django.contrib import admin
from import_export.admin import ExportMixin
from .models import file_processing

class FileProcessingAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['DIRECTORY','STATUS','DETAILS','DATE']
    #list_display_links = ('Record_Date',)
    search_fields = ('STATUS','DIRECTORY')
    list_per_page = 25
    list_filter = ('STATUS',)


admin.site.register(file_processing, FileProcessingAdmin)
