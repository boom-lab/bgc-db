from django.urls import path

from . import views, engineering_plots, diagnostics_plots, map, profile_explorer

urlpatterns = [
    #Float pages
    path('',views.newsite, name='newsite'),
    #path('',views.index, name='index'),
    path('index',views.index),
    path('floats_predeployment',views.floats_predeployment),
    path('float_detail',views.float_detail, name='float_detail'),
    path('float_tracking',views.float_tracking, name='float_tracking'),
    path('float_serial_no',views.float_serial_no, name='float_serial_no'),
    path('sensor_qc',views.sensor_qc_render, name='sensor_qc'),

    #Data pages
    path('profile_explorer',views.profile_explorer, name='profile_explorer'),
    path('map',views.display_map, name='map'),
    path('compare_latest_profiles',views.compare_latest_profiles, name='compare_latest_profiles'),
    path('cohort',views.cohort, name='cohort'),
    path('latest_profiles',views.latest_profiles, name='latest_profiles'),

    #Ajax - plot updates
    path('ajax/update_profile_plot', profile_explorer.update_profile_plot, name = "update_profile_plot"),
    path('ajax/blank_plot', profile_explorer.blank_plot, name = "blank_plot"),
    path('ajax/update_map', map.update_map, name = "update_map"),
    path('ajax/map_data', views.map_data, name = "map_data"),
    path('ajax/get_profiles_list', views.get_profiles_list, name = "get_profiles_list"), #using in React FE
    path('ajax/get_deployments_list', views.get_deployments_list, name = "get_deployments_list"), #using in React FE
    path('ajax/update_float_detail_plot', engineering_plots.update_select_plot, name = "update_select_plot"),
    path('ajax/cohort_data', views.cohort_data, name = "cohort_data"),
    path('ajax/update_latest_profiles_plots', diagnostics_plots.update_latest_profiles_plots, name = "update_latest_profiles_plots"),
    path('ajax/update_compare_latest_profiles', diagnostics_plots.update_compare_latest_profiles, name = "update_compare_latest_profiles"),

    #New front end - Data table pages
    path('FE/sensor_qc_data', views.GetSensorQCdata.as_view(), name="sensor_qc_data"),
    path('FE/sn_data', views.serial_number_data, name="sn_data"),
    path('FE/tracking_data', views.GetTrackingData.as_view(), name="tracking_data"),
    path('FE/float_detail', views.float_detail_FE, name="float_detail"),

    #New front end - React - data for plots and map
    path('FE/profile_explorer_data', views.profile_explorer_data, name="profile_explorer_data"),
    path('FE/latest_profiles_data', views.latest_profiles_data, name="latest_profiles_data"),
    path('FE/all_profiles_data', views.all_profiles_data, name="all_profiles_data"),
    path('FE/compare_latest_profiles_data', views.compare_latest_profiles_data, name="compare_latest_profiles_data"),
    path('FE/map_data', views.map_data_FE, name = "map_data"),
    
]