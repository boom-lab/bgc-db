from django.conf.urls import url
from deployments import views

from django.urls import path

urlpatterns = [ 
    url(r'^api/metadata', views.PostUpdate.as_view()), #token, patch put
    url(r'^api/deployment_metadata', views.GetDeploymentMeta.as_view()),#public, get
    url('api/wmo/', views.get_wmo, name='getwmo'),
    url('api/cal', views.get_cal, name='getcal'),
    url('api/locations', views.get_locations, name='getlocations'),
    url(r'^api/wmo_assigned', views.wmo_assigned),#public, get
]