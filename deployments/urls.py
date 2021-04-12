from django.conf.urls import url 
from deployments import views
#from .views import metadata_file
from django.urls import path

urlpatterns = [ 
    url(r'^api/deployments$', views.deployment_view),
    #path('export/', metadata_file, name='metadata_file'),
]
