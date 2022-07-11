from django.urls import path
from .views import Sensors, GetSensorMeta
 
urlpatterns = [ 
    path('api/sensors', Sensors.as_view()), #Token, patch or post
    path('api/sensor_metadata', GetSensorMeta.as_view()), #public, get
]
