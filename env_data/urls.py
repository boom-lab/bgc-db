from django.urls import path
from env_data import views

urlpatterns = [ 
    path('api/continuous_data_get', views.GetConData.as_view()), #Public, get
    path('api/nitrate_continuous_data_get', views.GetNitrateConData.as_view()), #Public, get
    path('api/discrete_data_get', views.GetDisData.as_view()), #Public, get
    path('api/park_data_get', views.GetParkData.as_view()), #Public, get
    path('api/cycle_meta_get', views.GetCycleMeta.as_view()), #Public, get

    path('api/continuous_profile_delete', views.con_profile_delete), #Token, delete
    path('api/nitrate_continuous_profile_delete', views.nitrate_con_profile_delete), #Token, delete
    path('api/discrete_profile_delete', views.dis_profile_delete), #Toeken, delete
    path('api/park_delete', views.park_delete), #Token, delete
    path('api/cycle_metadata_delete', views.cycle_metadata_delete), #Token, delete
    path('api/mission_reported_delete', views.mission_reported_delete), #Token, delete

    path('api/continuous_profile_stats', views.continuous_profile_stats), #Public, get
    path('api/discrete_profile_stats', views.dis_profile_stats), #Public, get
    path('api/processing/cycle_meta_update', views.CycleMetaUpdate.as_view()), #Token, post and patch
    
    
]
