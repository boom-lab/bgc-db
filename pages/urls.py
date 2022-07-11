from django.urls import path, re_path

from . import views

urlpatterns = [
    #New front end - Data table pages
    path('FE/sensor_qc_data', views.GetSensorQCdata.as_view(), name="sensor_qc_data"),
    path('FE/sn_data', views.serial_number_data, name="sn_data"),
    path('FE/tracking_data', views.GetTrackingData.as_view(), name="tracking_data"),
    path('FE/float_detail', views.float_detail, name="float_detail"),

    #New front end - React - data for plots and map
    path('FE/profile_explorer_data', views.profile_explorer_data, name="profile_explorer_data"),
    path('FE/latest_profiles_data', views.latest_profiles_data, name="latest_profiles_data"),
    path('FE/all_profiles_data', views.all_profiles_data, name="all_profiles_data"),
    path('FE/compare_latest_profiles_data', views.compare_latest_profiles_data, name="compare_latest_profiles_data"),
    path('FE/map_data', views.map_data, name = "map_data"),

    #Selector lists
    path('FE/get_profiles_list', views.get_profiles_list, name = "get_profiles_list"),
    path('FE/get_deployments_list', views.get_deployments_list, name = "get_deployments_list"),

    #Redirect all other requests to front end site
    re_path(r'.*',views.newsite, name='newsite'),
    
]