from django.conf.urls import url 
from env_data import views

urlpatterns = [ 
    url(r'api/continuous_profile$', views.con_profile_view), #Token, delete
    url(r'api/continuous_profile_stats$', views.continuous_profile_stats), #Public, get
    url(r'api/discrete_profile$', views.dis_profile_view), #Toeken, delete
    url(r'api/discrete_profile_stats$', views.dis_profile_stats), #Public, get
    url('api/park', views.park_view), #Token, delete
    url('api/cycle_metadata', views.cycle_metadata_view), #Token, delete
    url('api/cycle_meta_get', views.CycleMetaGet.as_view()), #Public, get
    url('api/processing/cycle_meta_update', views.CycleMetaUpdate.as_view()), #Token, post and patch
    url('api/mission_reported', views.mission_reported_view), #Token, delete
    
]
