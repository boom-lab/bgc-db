from django.shortcuts import render
from deployments.models import deployment
from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np
from django.http import JsonResponse

from env_data.models import continuous_profile, cycle_metadata
from .plot_helpers import *
import json
import pandas as pd

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


def map(request):
    return render(request, 'pages/map.html')


def update_profile_plot(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the selections
        profiles = request.GET.getlist("profiles[]", None)
        bot_var = request.GET.get("bot_var", None)
        top_var = request.GET.get("top_var", None)
        
        fig = go.Figure()
        
        for profile in profiles:
            #Create queries and convert to list
            PRES = continuous_profile.objects.filter(PROFILE_METADATA=profile).all().values_list('PRES', flat=True)
            bot = continuous_profile.objects.filter(PROFILE_METADATA=profile).all().values_list(bot_var, flat=True)


            #Convert lists to arrays
            bot_data = np.array(bot)
            y_data = np.array(PRES)*-1

            add_bottom_trace(fig, bot_data, y_data)

            # Formatting
            fig.update_layout(
                template = "ggplot2",
                xaxis = {'title':var_translation[bot_var]},
                yaxis = {'title':var_translation["PRES"]},
                font = {"size":15},
                height=800,
                width=1200,
                showlegend=False,
                margin={'t': 0, 'l':0,'r':0,'b':0},
                yaxis_range=[-1000,0],
            )

            if top_var:
                top = continuous_profile.objects.filter(PROFILE_METADATA=profile).all().values_list(top_var, flat=True)
                top_data = np.array(top)
                add_top_trace(fig, top_data, y_data)
                
                #Top axis formatting
                fig.update_layout(
                    xaxis2=dict(
                        title=var_translation[top_var],
                        titlefont=dict(
                            color="#9467bd"
                        ),
                        tickfont=dict(
                            color="#9467bd"
                        ),
                        anchor="free",
                        overlaying="x",
                        side="top",
                        position=1
                    ),
                    showlegend=False
                )

        plot_div = plot(fig,output_type='div', include_plotlyjs=False)

        return JsonResponse({'plot_div': plot_div }, status = 200)

    return JsonResponse({}, status = 400)

def update_map(request):
    if request.is_ajax and request.method == "GET":
        # get the selections
        deployments = request.GET.getlist("deployments[]", None)

        fig = go.Figure(go.Scattergeo())

        for d in deployments:
            lat = cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).all().values_list('GpsLat', flat=True)
            lon = cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).all().values_list('GpsLong', flat=True)
            print(lat)
            #Hover data
            #hov_data = np.stack((info_sub['ProfileId'], info_sub['TimeStartProfile_str'], info_sub['gps_lat'], info_sub['gps_lon'] ),axis = -1)

            fig.add_trace(go.Scattermapbox(
                mode = "lines",
                lon = list(lon),
                lat = list(lat),
                marker = {'size': 10},
                name = d,
                #customdata = hov_data,
                #hovertemplate ='Profile: %{customdata[0]}<br>Profile Start: %{customdata[1]}<br>Lat: %{customdata[2]}<br>Long: %{customdata[3]}',
            ))

        fig.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            height=800,
            autosize=True,
            hovermode='closest',
            mapbox = {
            'center': {'lon': 10, 'lat': 10},
            'style': "mapbox://styles/randerson5726/cklttcu382rbf17ljhunibjse",
            'accesstoken':'pk.eyJ1IjoicmFuZGVyc29uNTcyNiIsImEiOiJjanl5b2E0NTUxMGR5M25vN2xha2E4aHI1In0.xXUPHJrf_Shr6JX6u5X5cg',
            'center': {'lon': -36, 'lat': 39},
            'zoom': 3.5}
        )

        map_div = plot(fig,output_type='div', include_plotlyjs=False)

        return JsonResponse({'map_div': map_div }, status = 200)

    return JsonResponse({}, status = 400)