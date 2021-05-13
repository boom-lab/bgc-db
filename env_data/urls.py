from django.conf.urls import url 
from django.urls import path
from env_data import views

urlpatterns = [ 
    url('api/continuous_profile_test', views.con_profile),

    path('api/continuous_profile_delete/<str:PROFILE_ID>/', views.ConProfileDelete.as_view()),
    url('api/continuous_profile', views.ConProfile.as_view()),
    path('api/discrete_profile_delete/<str:PROFILE_ID>/', views.DisProfileDelete.as_view()),
    url('api/discrete_profile', views.DisProfile.as_view()),
    path('api/park_delete/<str:PROFILE_ID>/', views.ParkDelete.as_view()),
    url('api/park', views.Park.as_view()),
    path('api/cycle_metadata_delete/<str:PROFILE_ID>/', views.CycleMetaDelete().as_view()),
    url('api/cycle_metadata', views.CycleMeta().as_view()),
    path('api/mission_reported_delete/<str:PROFILE_ID>/', views.MissionReportedDelete().as_view()),
    url('api/mission_reported/', views.MissionReported().as_view()),
]
