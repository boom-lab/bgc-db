from django.urls import path
from deployments import views

urlpatterns = [ 
    path('api/metadata', views.PostUpdate.as_view()), #token, patch put
    path('api/deployment_metadata', views.GetDeploymentMeta.as_view()),#public, get
    path('api/wmo/', views.get_wmo, name='getwmo'), #public, get
    path('api/cal', views.get_cal, name='getcal'), #public, get
    path('api/locations', views.get_locations, name='getlocations'), #public, get
    path('api/wmo_assigned', views.wmo_assigned),#public, get
    path('api/latest_cycle',views.latest_cycle),#public, get
]