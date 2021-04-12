from django.conf.urls import url 
from missions import views
from .views import GetSensor, sensors_csv
from django.urls import path
 
urlpatterns = [ 
    url(r'^api/getsensor$', GetSensor.as_view()),
    path('test/sensors/export', sensors_csv, name='export'),
]
