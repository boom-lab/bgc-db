from django.conf.urls import url 
#from django.urls import path
from .views import GetSensors, update_suna_cal
 
urlpatterns = [ 
    url(r'^api/sensors$', GetSensors.as_view()),
    url('api/sensors/sunacal', update_suna_cal),
]
