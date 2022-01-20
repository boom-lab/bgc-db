from django.contrib import admin
from .models import deployment
from django.utils.safestring import mark_safe 
from django.urls import reverse
from django.conf.urls import re_path
from import_export.admin import ExportMixin

from .views import admin_detail_view, export_metadata

def Export_Metadata_File(modeladmin, request, queryset):
    ids = []
    for d in queryset:
        ids.append(d.id)
    return export_metadata(request, ids)


class DeploymentAdmin(ExportMixin, admin.ModelAdmin):
    all_fields = [field.name for field in deployment._meta.fields]

    list_display = ['detail_link', 'edit_link', 'event_link', 'mission_link'] + all_fields
    list_display_links = None
    list_filter = ('PLATFORM_TYPE','HISTORICAL')
    search_fields = ('FLOAT_SERIAL_NO','PLATFORM_NUMBER')
    list_per_page = 10
    actions = [Export_Metadata_File]


    #Custom detail link
    def detail_link(self, obj):
        admin_url = reverse('admin:detail_view', args=(obj.pk,))

        return mark_safe('<a href="{}">{}</a>'.format(
            admin_url,
            'Details'
        ))
    detail_link.short_description = 'Details'

    #Custom edit link
    def edit_link(self, obj):
        app = obj._meta.app_label
        model = obj._meta.model_name
        admin_url = reverse("admin:{}_{}_change".format(app, model),  args=(obj.pk,))

        return mark_safe('<a href="{}">Edit</a>'.format(
            admin_url
        ))
    edit_link.short_description = 'Edit'

    #Add event link
    def event_link(self, obj):
        admin_url = reverse("admin:logs_deployment_tracking_add")

        return mark_safe('<a href="{}">Add Event</a>'.format(admin_url + "?DEPLOYMENT=" + str(obj.pk)))
    event_link.short_description = 'Add Event'

    #Add mission link
    def mission_link(self, obj):
        admin_url = reverse("admin:missions_mission_add")

        return mark_safe('<a href="{}">Add Mission</a>'.format(admin_url + "?DEPLOYMENT=" + str(obj.pk)))
    mission_link.short_description = 'Add Mission'

    #Add custom detail view to urls
    def get_urls(self):
        urls = super(DeploymentAdmin, self).get_urls()
        my_urls = [
            re_path(r'^detail_view/(?P<entry_id>\d+)/$', self.admin_site.admin_view(admin_detail_view), 
                {'admin_site' :self.admin_site}, name='detail_view'), #detail view
            re_path(r'^export_metadata/(?P<entry_id>\d+)/$', self.admin_site.admin_view(export_metadata), name='export_metadata'), #export metadata
        ]
        return my_urls + urls




admin.site.register(deployment, DeploymentAdmin)