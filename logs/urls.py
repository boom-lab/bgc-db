from django.conf.urls import url 
from logs import views

urlpatterns = [
    url('api/processing/filestatus', views.get_file_status),
    url('api/processing/put', views.put_process_log)
]