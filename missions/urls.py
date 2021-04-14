from django.conf.urls import url 
from missions import views
 
urlpatterns = [ 
    url(r'^api/missions$', views.mission),
]
