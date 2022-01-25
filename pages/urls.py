from django.urls import path

from . import views, engineering_plots, diagnostics_plots, map, profile_explorer

urlpatterns = [
    path('',views.index, name='index'),
    path('index',views.index),
    path('floats_predeployment',views.floats_predeployment),
    path('profile_explorer',views.profile_explorer, name='profile_explorer'),
    path('compare_latest_profiles',views.compare_latest_profiles, name='compare_latest_profiles'),
    path('map',views.display_map, name='map'),
    path('float_detail',views.float_detail, name='float_detail'),
    path('float_tracking',views.float_tracking, name='float_tracking'),
    path('float_serial_no',views.float_serial_no, name='float_serial_no'),
    path('cohort',views.cohort, name='cohort'),
    path('latest_profiles',views.latest_profiles, name='latest_profiles'),
    path('ajax/update_profile_plot', profile_explorer.update_profile_plot, name = "update_profile_plot"),
    path('ajax/blank_plot', profile_explorer.blank_plot, name = "blank_plot"),
    path('ajax/update_map', map.update_map, name = "update_map"),
    path('ajax/get_profiles_list', views.get_profiles_list, name = "get_profiles_list"),
    path('ajax/get_deployments_list', views.get_deployments_list, name = "get_deployments_list"),
    path('ajax/update_float_detail_plot', engineering_plots.update_select_plot, name = "update_select_plot"),
    path('ajax/cohort_data', views.cohort_data, name = "cohort_data"),
    path('ajax/update_latest_profiles_plots', diagnostics_plots.update_latest_profiles_plots, name = "update_latest_profiles_plots"),
    path('ajax/update_compare_latest_profiles', diagnostics_plots.update_compare_latest_profiles, name = "update_compare_latest_profiles"),
]