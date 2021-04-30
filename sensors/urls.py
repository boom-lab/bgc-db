from django.conf.urls import url 
from django.urls import path
from .views import GetSensors, UpdateSensors
 
urlpatterns = [ 
    url(r'^api/sensors$', GetSensors.as_view()),
    path('api/sensors/update/<int:SENSOR_SERIAL_NO>', UpdateSensors.as_view()),
]
