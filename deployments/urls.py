from django.conf.urls import re_path
from deployments import views

from django.urls import path

urlpatterns = [ 
    re_path(r'^api/metadata', views.PostUpdate.as_view()), #token, patch put
    re_path(r'^api/deployment_metadata', views.GetDeploymentMeta.as_view()),#public, get
    re_path('api/wmo/', views.get_wmo, name='getwmo'), #public, get
    re_path('api/cal', views.get_cal, name='getcal'), #public, get
    re_path('api/locations', views.get_locations, name='getlocations'), #public, get
    re_path(r'^api/wmo_assigned', views.wmo_assigned),#public, get
    re_path(r'api/latest_cycle$',views.latest_cycle),#public, get
]