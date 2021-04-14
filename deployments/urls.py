from django.conf.urls import url 
from deployments import views
from django.urls import path

urlpatterns = [ 
    url(r'^api/deployments$', views.deployment_view), #adding data
    #path('api/deployments/wmo/<int:serial_number>/', views.get_wmo), # get wmo from serial number
    url('^api/deployments/wmo/$', views.get_wmo, name='getwmo')
]
