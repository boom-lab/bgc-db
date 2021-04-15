from django.conf.urls import url 
from deployments import views

#from django.urls import path

urlpatterns = [ 
    url('api/metadata', views.MetadataView.as_view()),
    url('api/current_metadata', views.GetCrtMetadata.as_view()),
    url('api/deployments/wmo/', views.get_wmo, name='getwmo'),
]
