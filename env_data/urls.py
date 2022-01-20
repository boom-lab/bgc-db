from django.conf.urls import re_path
from env_data import views

urlpatterns = [ 
    re_path(r'api/continuous_data_get$', views.GetConData.as_view()), #Public, get
    re_path(r'api/discrete_data_get$', views.GetDisData.as_view()), #Public, get
    re_path(r'api/park_data_get$', views.GetParkData.as_view()), #Public, get
    re_path(r'api/cycle_meta_get$', views.GetCycleMeta.as_view()), #Public, get

    re_path(r'api/continuous_profile_delete$', views.con_profile_delete), #Token, delete
    re_path(r'api/discrete_profile_delete$', views.dis_profile_delete), #Toeken, delete
    re_path(r'api/park_delete$', views.park_delete), #Token, delete
    re_path(r'api/cycle_metadata_delete$', views.cycle_metadata_delete), #Token, delete
    re_path(r'api/mission_reported_delete$', views.mission_reported_delete), #Token, delete

    re_path(r'api/continuous_profile_stats$', views.continuous_profile_stats), #Public, get
    re_path(r'api/discrete_profile_stats$', views.dis_profile_stats), #Public, get
    re_path(r'api/processing/cycle_meta_update$', views.CycleMetaUpdate.as_view()), #Token, post and patch
    
    
]
