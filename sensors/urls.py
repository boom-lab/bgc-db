from django.conf.urls import url 
#from django.urls import path
from .views import GetSensors
 
urlpatterns = [ 
    url(r'^api/sensors$', GetSensors.as_view()),
]
