from django.conf.urls import url 
from env_data import views

urlpatterns = [ 
    url('api/continuous_profile', views.GetConProfile.as_view()),
    url('api/discrete_profile', views.GetDisProfile.as_view()),
    url('api/park', views.GetPark.as_view()),
    url('api/cycle_metadata', views.GetCycleMeta().as_view()),
    url('api/mission_reported', views.GetMissionReported().as_view()),
]
