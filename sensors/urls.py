from django.conf.urls import re_path
from .views import Sensors, GetSensorMeta
 
urlpatterns = [ 
    re_path(r'^api/sensors$', Sensors.as_view()), #Token, patch or post
    re_path(r'^api/sensor_metadata', GetSensorMeta.as_view()), #public, get
]
