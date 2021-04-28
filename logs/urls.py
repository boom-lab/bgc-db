from django.conf.urls import url 
from logs import views

urlpatterns = [
    url('api/processing/success', views.get_success_files),
    url('api/processing/put', views.put_process_log)
]