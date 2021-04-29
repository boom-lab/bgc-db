from django.conf.urls import url 
from logs import views

urlpatterns = [
    url('api/processing/ignore', views.get_ignore_files),
    url('api/processing/put', views.put_process_log)
]