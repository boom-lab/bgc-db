from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('index',views.index),
    path('status',views.status, name='status'),
    path('profile_plot',views.profile_plot, name='profile_plot'),
    path('map',views.display_map, name='map'),
    path('ajax/update_profile_plot', views.update_profile_plot, name = "update_profile_plot"),
    path('ajax/update_map', views.update_map, name = "update_map"),
    path('ajax/get_profiles_list', views.get_profiles_list, name = "get_profiles_list"),
    path('ajax/get_deployments_list', views.get_deployments_list, name = "get_deployments_list")
]