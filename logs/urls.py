from django.urls import path
from logs import views

urlpatterns = [
    path('api/processing/filestatus', views.get_file_status), #Token, get
    path('api/processing/put', views.put_process_log) #Token, put
]