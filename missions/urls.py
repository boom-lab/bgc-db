from django.conf.urls import url 
from .views import export_NAVIS_mission_config
 
urlpatterns = [
    url(r'^export_mission_config/(?P<entry_id>\d+)/$', export_NAVIS_mission_config, name='export_metadata')
]
