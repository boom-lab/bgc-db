from django.urls import path

from . import views, engineering_plots, diagnostics_plots, map, profile_explorer

urlpatterns = [
    path('',views.index, name='index'),
    path('index',views.index),
    path('floats_predeployment',views.floats_predeployment),
    path('profile_explorer',views.profile_explorer, name='profile_explorer'),
    path('map',views.display_map, name='map'),
    path('float_detail',views.float_detail, name='float_detail'),
    path('float_tracking',views.float_tracking, name='float_tracking'),
    path('cohort',views.cohort, name='cohort'),
    path('cohort_latest',views.cohort_latest, name='cohort_latest'),
    path('ajax/update_profile_plot', profile_explorer.update_profile_plot, name = "update_profile_plot"),
    path('ajax/blank_plot', profile_explorer.blank_plot, name = "blank_plot"),
    path('ajax/update_map', map.update_map, name = "update_map"),
    path('ajax/get_profiles_list', views.get_profiles_list, name = "get_profiles_list"),
    path('ajax/get_deployments_list', views.get_deployments_list, name = "get_deployments_list"),
    path('ajax/update_float_detail_plot', engineering_plots.update_select_plot, name = "update_select_plot"),
    path('ajax/cohort_data', views.cohort_data, name = "cohort_data"),
    path('ajax/update_cohort_latest_plot', diagnostics_plots.update_cohort_latest_plot, name = "update_cohort_latest_plot"),
]