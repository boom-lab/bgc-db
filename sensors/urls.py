from django.conf.urls import url 
from django.urls import path
from .views import Sensors
 
urlpatterns = [ 
    url(r'^api/sensors$', Sensors.as_view()),
]
