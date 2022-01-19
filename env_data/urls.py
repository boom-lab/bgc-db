from django.conf.urls import url 
from env_data import views

urlpatterns = [ 
    url(r'api/continuous_data_get$', views.GetConData.as_view()), #Public, get
    url(r'api/discrete_data_get$', views.GetDisData.as_view()), #Public, get
    url(r'api/park_data_get$', views.GetParkData.as_view()), #Public, get
    url(r'api/cycle_meta_get$', views.GetCycleMeta.as_view()), #Public, get

    url(r'api/continuous_profile_delete$', views.con_profile_delete), #Token, delete
    url(r'api/discrete_profile_delete$', views.dis_profile_delete), #Toeken, delete
    url(r'api/park_delete$', views.park_delete), #Token, delete
    url(r'api/cycle_metadata_delete$', views.cycle_metadata_delete), #Token, delete
    url(r'api/mission_reported_delete$', views.mission_reported_delete), #Token, delete

    url(r'api/continuous_profile_stats$', views.continuous_profile_stats), #Public, get
    url(r'api/discrete_profile_stats$', views.dis_profile_stats), #Public, get
    url(r'api/processing/cycle_meta_update$', views.CycleMetaUpdate.as_view()), #Token, post and patch
    
    
]
