from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
import pandas as pd
import numpy as np
from plotly.offline import plot
import plotly.graph_objs as go

from deployments.models import deployment
from env_data.models import continuous_profile, cycle_metadata, discrete_profile
from .plot_helpers import add_bottom_trace, add_top_trace, var_translation
import pages.engineering_plots as ep

def index(request):
    deployments = deployment.objects.all()

    context = {
        'deployments': deployments,
    }
    return render(request, 'pages/index.html', context)

def profile_plot(request):
    return render(request, 'pages/profile_plot.html')

def cohort(request):
    return render(request, 'pages/cohort.html')

def display_map(request):
    return render(request, 'pages/map.html')

def float_detail(request):
    FLOAT_SERIAL_NO = request.GET.get('FLOAT_SERIAL_NO', None)
    PLATFORM_TYPE = request.GET.get('PLATFORM_TYPE', None)

    filters={}
    filters['DEPLOYMENT__FLOAT_SERIAL_NO'] = FLOAT_SERIAL_NO
    filters['DEPLOYMENT__PLATFORM_TYPE'] = PLATFORM_TYPE

    dfilters = {}
    dfilters['FLOAT_SERIAL_NO'] = FLOAT_SERIAL_NO
    dfilters['PLATFORM_TYPE'] = PLATFORM_TYPE
    dep = deployment.objects.get(**dfilters)

    n_reports = cycle_metadata.objects.filter(**filters).count()

    #If deployed
    if n_reports > 0:
        latest_cycle_meta = cycle_metadata.objects.filter(**filters).order_by("-GpsFixDate").first()

        abpres_plot = ep.single_var_plot(filters, "AirBladderPressure", y_label="Pressure", legend_label="Air Bladder Pressure")
        buoy_pump_time_plot = ep.single_var_plot(filters, "BuoyancyPumpOnTime", y_label="Time", 
            legend_label="Buoyancy Pump On Time")

        calc={}
        if latest_cycle_meta.MSG_BYTES:
            calc['MSG_KB'] = round(latest_cycle_meta.MSG_BYTES/1000,1)
        if latest_cycle_meta.ISUS_BYTES:
            calc['ISUS_KB'] = round(latest_cycle_meta.ISUS_BYTES/1000,1)
        if latest_cycle_meta.LOG_BYTES:
            calc['LOG_KB'] = round(latest_cycle_meta.LOG_BYTES/1000,1)
        if latest_cycle_meta.MSG_BYTES and latest_cycle_meta.ISUS_BYTES and latest_cycle_meta.LOG_BYTES:
            calc['TOTAL'] = calc['MSG_KB']+calc['ISUS_KB']+calc['LOG_KB']

        context = {
            'cycle_metadata': latest_cycle_meta,
            'calc':calc,
            'deployment':dep,
            'battery_plot':ep.volts_plot(filters),
            'amps_plot':ep.amps_plot(filters),
            'buoyancy_plot':ep.buoyancy_position_plot(filters),
            'air_bladder_pres_plot': abpres_plot,
            'buoy_pump_time_plot': buoy_pump_time_plot,
            'duration_plot':ep.duration_plot(filters),
            'con_attempt_plot':ep.con_attempt_plot(filters),
            'upload_attempt_plot':ep.upload_attempt_plot(filters),
            'surface_duration_plot':ep.surface_duration_plot(filters),
            'park_pres_plot':ep.park_pres_plot(filters)
        }
        return render(request, 'pages/float_detail.html', context)
    else: #Pre deployment
        context = {
            'cycle_metadata': None,
            'calc':None,
            'deployment':dep,
        }
        return render(request, 'pages/float_detail.html', context)


def update_profile_plot(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the selections
        profiles = request.GET.getlist("profiles[]", None)
        bot_var = request.GET.get("bot_var", None)
        top_var = request.GET.get("top_var", None)
        cont = request.GET.get("cont", None) == 'true'
        dis = request.GET.get("dis", None) == 'true'
        fig = go.Figure()
        
        for profile in profiles:

            #Hover data
            hov = pd.DataFrame()
            hov['float_profile'] = list(continuous_profile.objects.filter(PROFILE_ID=profile).all().values_list('PROFILE_ID', flat=True))
            hov['profile'] = hov['float_profile'].str.split('.').str[1]
            hov['float'] = hov['float_profile'].str.split('.').str[0]
            hov_data = hov.values.tolist()
            wmo = profile.split(".")[0]

            #Continuous data
            if cont and (bot_var != "NITRATE"):
                #Continuous data queries and convert to list
                PRES = continuous_profile.objects.filter(PROFILE_ID=profile).all().values_list('PRES', flat=True)
                bot = continuous_profile.objects.filter(PROFILE_ID=profile).all().values_list(bot_var, flat=True)

                #Convert lists to arrays
                bot_data = np.array(bot)
                y_data = np.array(PRES)*-1

                add_bottom_trace(fig, bot_data, y_data, hov_data, wmo)

            #Top axis continuous plotting
            if cont and top_var and (top_var != "NITRATE"):
                top = continuous_profile.objects.filter(PROFILE_ID=profile).all().values_list(top_var, flat=True)
                top_data = np.array(top)

                add_top_trace(fig, top_data, y_data, top_var, hov_data, wmo)

            #discrete data
            if dis:
                #Discrete data queries and convert to list
                PRES = discrete_profile.objects.filter(PROFILE_ID=profile).all().values_list('PRES', flat=True)
                bot = discrete_profile.objects.filter(PROFILE_ID=profile).all().values_list(bot_var, flat=True)

                #Convert lists to arrays
                bot_data = np.array(bot)
                y_data = np.array(PRES)*-1

                add_bottom_trace(fig, bot_data, y_data, hov_data, wmo, mode="markers")

                #Top axis discrete plotting
                if top_var:
                    top = discrete_profile.objects.filter(PROFILE_ID=profile).all().values_list(top_var, flat=True)
                    top_data = np.array(top)
                    add_top_trace(fig, top_data, y_data, top_var, hov_data, wmo, mode="markers")          
            
            # Formatting
            fig.update_layout(
                template = "ggplot2",
                xaxis = {'title':var_translation[bot_var]},
                yaxis = {'title':var_translation["PRES"]},
                font = {"size":15},
                height=800,
                width=1000,
                showlegend=False,
                margin={'t': 0, 'l':0,'r':0,'b':0},
                #yaxis_range=[-2000,0],
            )

        #Metadata for table
        table_context = cycle_metadata.objects.filter(PROFILE_ID__in=profiles).all()
        meta_table = render_to_string('partials/plot_table.html', context = {'metadatas':table_context}, request = request)

        plot_div = plot(fig,output_type='div', include_plotlyjs=False, config= {'displaylogo': False, 'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})

        return JsonResponse({'plot_div': plot_div, 'meta_table':meta_table}, status = 200)

    return JsonResponse({}, status = 400)

def update_map(request):
    
    if request.is_ajax and request.method == "GET":
        # get the selections
        deployments = request.GET.getlist("deployments[]", None)

        fig = go.Figure(go.Scattergeo())

        for d in deployments:
            lat = list(cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').all().values_list('GpsLat', flat=True))
            lon = list(cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').all().values_list('GpsLong', flat=True))
            profile_id = list(cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').all().values_list('PROFILE_ID', flat=True))
            time_start_p = pd.Series(cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').all().values_list('TimeStartTelemetry', flat=True))
            time_start_p_human = time_start_p.dt.strftime('%Y-%m-%d %H:%M')
            time_start_p_human = time_start_p_human.replace(np.nan, '')
            #Hover data
            hov_data = np.stack((profile_id, time_start_p_human, lat, lon),axis = -1)

            fig.add_trace(go.Scattermapbox(
                mode = "lines",
                lon = lon,
                lat = lat,
                marker = {'size': 10},
                name = d,
                customdata = hov_data,
                hovertemplate ='Profile: %{customdata[0]}<br>Profile Start: %{customdata[1]}<br>Lat: %{customdata[2]}<br>Long: %{customdata[3]}',
                showlegend=False
            ))

        fig.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            height=900,
            autosize=True,
            hovermode='closest',
            mapbox = {
                'style': "mapbox://styles/randerson5726/cklttcu382rbf17ljhunibjse",
                'accesstoken':'pk.eyJ1IjoicmFuZGVyc29uNTcyNiIsImEiOiJjanl5b2E0NTUxMGR5M25vN2xha2E4aHI1In0.xXUPHJrf_Shr6JX6u5X5cg',
                'center': {'lon': -36, 'lat': 39},
                'zoom': 3.5
            },
        )

        map_div = plot(fig,output_type='div', include_plotlyjs=False, config= {'displaylogo': False, 'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})

        return JsonResponse({'map_div': map_div }, status = 200)

    return JsonResponse({}, status = 400)


def get_profiles_list(request):
    # for populating selector dropdown
    if request.is_ajax and request.method == "GET":
        profile_id = cycle_metadata.objects.all().values_list('PROFILE_ID', flat=True)

        return JsonResponse({'profiles': list(profile_id) }, status = 200)

    return JsonResponse({}, status = 400)


def get_deployments_list(request):
    # for populationg selector dropdown
    if request.is_ajax and request.method == "GET":
        platform_number = deployment.objects.all().values_list('PLATFORM_NUMBER', flat=True)
        float_serial_no = deployment.objects.all().values_list('FLOAT_SERIAL_NO', flat=True)

        res = []
        for i, item in enumerate(platform_number):
            res.append({'PLATFORM_NUMBER':item, "LABEL":"WMO: " + str(item) + " SN:" + str(float_serial_no[i])})

        return JsonResponse({"deployments":res}, status = 200)

    return JsonResponse({}, status = 400)