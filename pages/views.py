from django.shortcuts import render
from deployments.models import deployment
from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np
from django.http import JsonResponse
import pandas as pd
from django.template.loader import render_to_string

from env_data.models import continuous_profile, cycle_metadata, discrete_profile
from .plot_helpers import add_bottom_trace, add_top_trace, var_translation

def index(request):
    return render(request, 'pages/index.html')

def status(request):
    deployments = deployment.objects.all()
    context = {
        'deployments': deployments,
    }
    return render(request, 'pages/status.html', context)

def profile_plot(request):
    return render(request, 'pages/profile_plot.html')


def display_map(request):
    return render(request, 'pages/map.html')

def battery_plot(filters):
    profile_id = cycle_metadata.objects.filter(**filters).order_by("ProfileId").values_list('ProfileId', flat=True)
    quiescent_volts = cycle_metadata.objects.filter(**filters).order_by("ProfileId").values_list('QuiescentVolts', flat=True)
    sbe41cp_volts = cycle_metadata.objects.filter(**filters).order_by("ProfileId").values_list('Sbe41cpVolts', flat=True)
    date = cycle_metadata.objects.filter(**filters).order_by("ProfileId").values_list('GpsFixDate', flat=True)


    hov = pd.DataFrame()
    hov["GpsFixDate"] = list(date)
    hov["GpsFixDate"] = hov.GpsFixDate.dt.strftime('%Y-%m-%d')
    hov_data = hov.values.tolist()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=np.array(profile_id),
            y=np.array(quiescent_volts),
            mode='lines',
            marker = {
                'size':8,
                'color': "#1f77b4",
                'symbol':'circle',
                'line':{'width':0}
            },
            customdata = hov_data,
            hovertemplate ='%{customdata[0]}',
            name="Quiescent Volts"
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=np.array(profile_id),
            y=np.array(sbe41cp_volts),
            mode='lines',
            marker = {
                'size':8,
                'color': "#ff7f0e",
                'symbol':'circle',
                'line':{'width':0}
            },
            customdata = hov_data,
            hovertemplate ='%{customdata[0]}',
            yaxis="y2",
            name="SBE41cp"
        ),
    )
    
    # Formatting
    fig.update_layout(
        template = "ggplot2",
        title = "Battery",
        xaxis = {'title':"Cycle"},
        #yaxis = {'title':"Quiescent Voltage"},
        font = {"size":15},
        height=500,
        showlegend=False,
        margin={'t': 70, 'l':0,'r':0,'b':0},
        #yaxis_range=[8,12]
        yaxis=dict(
            title="Quiescent Volts",
            range=[8,12],
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis2=dict(
            title="SBE41cp Volts",
            range=[8,12],
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            ),
            anchor="free",
            overlaying="y",
            side="right",
            position=1
        ),
    )

    plot_div = plot(fig,output_type='div', include_plotlyjs=False)  
    return plot_div

def float_detail(request):
    FLOAT_SERIAL_NO = request.GET.get('FLOAT_SERIAL_NO', None)
    PLATFORM_TYPE = request.GET.get('PLATFORM_TYPE', None)

    filters={}
    filters['DEPLOYMENT__FLOAT_SERIAL_NO'] = FLOAT_SERIAL_NO
    filters['DEPLOYMENT__PLATFORM_TYPE'] = PLATFORM_TYPE
    latest_cycle_meta = cycle_metadata.objects.filter(**filters).order_by("-GpsFixDate").first()

    dfilters = {}
    dfilters['FLOAT_SERIAL_NO'] = FLOAT_SERIAL_NO
    dfilters['PLATFORM_TYPE'] = PLATFORM_TYPE
    dep = deployment.objects.get(**dfilters)
    
    bat_plot = battery_plot(filters)

    context = {
        'cycle_metadata': latest_cycle_meta,
        'deployment':dep,
        'battery_plot':bat_plot
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
            hov['float_profile'] = list(continuous_profile.objects.filter(PROFILE_METADATA=profile).all().values_list('MISSION', flat=True))
            hov['profile'] = hov['float_profile'].str.split('.').str[1]
            hov['float'] = hov['float_profile'].str.split('.').str[0]
            hov_data = hov.values.tolist()
            wmo = profile.split(".")[0]



            #Continuous data
            if cont and (bot_var != "NITRATE"):
                #Continuous data queries and convert to list
                PRES = continuous_profile.objects.filter(PROFILE_METADATA=profile).all().values_list('PRES', flat=True)
                bot = continuous_profile.objects.filter(PROFILE_METADATA=profile).all().values_list(bot_var, flat=True)

                #Convert lists to arrays
                bot_data = np.array(bot)
                y_data = np.array(PRES)*-1

                add_bottom_trace(fig, bot_data, y_data, hov_data, wmo)

            #Top axis continuous plotting
            if cont and top_var and (top_var != "NITRATE"):
                top = continuous_profile.objects.filter(PROFILE_METADATA=profile).all().values_list(top_var, flat=True)
                top_data = np.array(top)

                add_top_trace(fig, top_data, y_data, top_var, hov_data, wmo)

            #discrete data
            if dis:
                #Discrete data queries and convert to list
                PRES = discrete_profile.objects.filter(PROFILE_METADATA=profile).all().values_list('PRES', flat=True)
                bot = discrete_profile.objects.filter(PROFILE_METADATA=profile).all().values_list(bot_var, flat=True)

                #Convert lists to arrays
                bot_data = np.array(bot)
                y_data = np.array(PRES)*-1

                add_bottom_trace(fig, bot_data, y_data, hov_data, wmo, mode="markers")

                #Top axis discrete plotting
                if top_var:
                    top = discrete_profile.objects.filter(PROFILE_METADATA=profile).all().values_list(top_var, flat=True)
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

        plot_div = plot(fig,output_type='div', include_plotlyjs=False)

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

        map_div = plot(fig,output_type='div', include_plotlyjs=False)

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