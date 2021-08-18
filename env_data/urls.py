from django.conf.urls import url 
from env_data import views

urlpatterns = [ 
    url('api/continuous_profile', views.con_profile_view), #Token, delete
    url('api/discrete_profile', views.dis_profile_view), #Toeken, delete
    url('api/park', views.park_view), #Token, delete
    url('api/cycle_metadata', views.cycle_metadata_view), #Token, delete
    url('api/mission_reported', views.mission_reported_view), #Token, delete
    url('api/processing/cycle_meta_update', views.CycleMetaUpdate.as_view()) #Token, post and patch
]
