from django.http import JsonResponse
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np

from env_data.models import cycle_metadata


def update_map(request):
    
    if request.is_ajax and request.method == "GET":
        # get the selections
        deployments = request.GET.getlist("deployments[]", None)

        fig = go.Figure(go.Scattergeo())

        for d in deployments:
            #Data for traces
            lat = list(cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').all().values_list('GpsLat', flat=True))
            lon = list(cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').all().values_list('GpsLong', flat=True))
            profile_id = list(cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').all().values_list('PROFILE_ID', flat=True))
            time_start_p = pd.Series(cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by(
                '-GpsFixDate').all().values_list('TimeStartTelemetry', flat=True))
            time_start_p_human = time_start_p.dt.strftime('%Y-%m-%d %H:%M')
            time_start_p_human = time_start_p_human.replace(np.nan, '')
            #Hover data
            hov_data = np.stack((profile_id, time_start_p_human, lat, lon),axis = -1)

            #Data for current location points
            current_lat = (cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').first().GpsLat)
            current_lon = (cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER=d).order_by('-GpsFixDate').first().GpsLong)

            #Traces
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

            #Current Location
            fig.add_trace(go.Scattermapbox(
                mode = "markers",
                lon = (current_lon,),
                lat = (current_lat,),
                marker = dict( size=8, color='rgb(209,62,36)'),
                name = d,
                hoverinfo='skip',
                #customdata = hov_data,
                #hovertemplate ='Profile: %{customdata[0]}<br>Profile Start: %{customdata[1]}<br>Lat: %{customdata[2]}<br>Long: %{customdata[3]}',
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

        map_div = plot(fig,output_type='div', include_plotlyjs=False, config= {'displaylogo': False, 
            'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})

        return JsonResponse({'map_div': map_div }, status = 200)

    return JsonResponse({}, status = 400)
