from django.conf.urls import url 
from .views import GetMissions, AddMissions
 
urlpatterns = [ 
    url(r'^api/missions$', GetMissions.as_view()),
    url(r'^api/add_mission$', AddMissions.as_view()),
]
