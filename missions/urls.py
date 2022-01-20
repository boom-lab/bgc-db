from django.conf.urls import re_path
from .views import export_NAVIS_mission_config
 
urlpatterns = [
    re_path(r'^export_mission_config/(?P<entry_id>\d+)/$', export_NAVIS_mission_config, name='export_metadata')
]
