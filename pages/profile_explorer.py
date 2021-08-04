from django.http import JsonResponse
from django.template.loader import render_to_string
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from plotly.offline import plot

from env_data.models import continuous_profile, cycle_metadata, discrete_profile


continuous_exclude_vars = ['NITRATE','VRS_PH','VK_PH','IB_PH','IK_PH']

def add_bottom_trace(fig, bot_data, y_data, hov_data, wmo, mode='lines'):
    # Bottom x axis trace
    fig.add_trace(
        go.Scatter(
            x=bot_data,
            y=y_data,
            mode=mode,
            marker = {
                'size':8,
                'color': '#000000',
                'symbol':'circle',
                'line':{'width':0}
            },
            customdata = hov_data,
            hovertemplate ='Profile: %{customdata[1]}',
            xaxis="x",
            name="WMO:"+wmo
        ),
    )

def add_top_trace(fig, top_data, y_data, top_var, hov_data, wmo, mode='lines',):
    fig.add_trace(
        go.Scatter(
            x=top_data,
            y=y_data,
            mode=mode,
            marker = {
                'size':8,
                'color': "#9467bd",
                'symbol':'circle',
                'line':{'width':0}
            },
            customdata = hov_data,
            hovertemplate ='Profile: %{customdata[1]}',
            xaxis="x2",
            name="WMO:"+wmo
        ),
    )
    
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


var_translation = {
    "TEMP":"Temperature (°C)",
    "PRES":"Pressure (dbar)",
    "PSAL": "Practical Salinity",
    "DOXY":"Dissolved Oxygen (μmol/kg)",
    "CHLA":"Chlorophyll a (mg/m<sup>3</sup>)",
    "BBP700":"Particle backscattering at 700 nm (m<sup>-1</sup>)",
    "PH_IN_SITU_TOTAL":"pH total scale",
    "NITRATE":"Nitrate (μmol/kg)",
    "CDOM":"Coloured dissolved organic matter (ppb)",
    "VRS_PH":"pH Vrs",
    "VK_PH":"pH Vk",
    "IB_PH":"pH Ib",
    "IK_PH":"pH Ik"
}

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
            if cont:
                PRES = continuous_profile.objects.filter(PROFILE_ID=profile).all().values_list('PRES', flat=True)
                y_data = np.array(PRES)*-1
                
                #Bottom Axis
                if bot_var not in continuous_exclude_vars:
                    #Continuous data queries and convert to list
                    bot = continuous_profile.objects.filter(PROFILE_ID=profile).all().values_list(bot_var, flat=True)

                    #Convert lists to arrays
                    bot_data = np.array(bot)

                    add_bottom_trace(fig, bot_data, y_data, hov_data, wmo)

                #Continuous top axis
                if top_var and (top_var not in continuous_exclude_vars):
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
                xaxis = dict(
                    title=var_translation[bot_var],
                    showline=True,
                    linewidth=1,
                    linecolor="#000000",
                    mirror=True
                ),
                yaxis = dict(
                    title=var_translation["PRES"],
                    showline=True,
                    linewidth=1,
                    linecolor="#000000",
                    mirror=True
                ),
                font = {"size":12},
                height=800,
                width=1000,
                showlegend=False,
                margin={'t': 0, 'l':0,'r':0,'b':0},
                #yaxis_range=[-2000,0],
            )

        #Metadata for table
        table_context = cycle_metadata.objects.filter(PROFILE_ID__in=profiles).all()
        meta_table = render_to_string('partials/plot_table.html', context = {'metadatas':table_context}, request = request)

        plot_div = plot(fig,output_type='div', include_plotlyjs=False, config= {'displaylogo': False, 
            'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})

        return JsonResponse({'plot_div': plot_div, 'meta_table':meta_table}, status = 200)

    return JsonResponse({}, status = 400)

def blank_plot(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        fig = go.Figure()
        
        # Formatting
        fig.update_layout(
            template = "ggplot2",
            xaxis = dict(
                showline=True,
                linewidth=1,
                linecolor="#000000",
                mirror=True
            ),
            yaxis = dict(
                title=var_translation["PRES"],
                showline=True,
                linewidth=1,
                linecolor="#000000",
                mirror=True
            ),
            font = {"size":12},
            height=800,
            width=1000,
            showlegend=False,
            margin={'t': 0, 'l':0,'r':0,'b':0},
            #yaxis_range=[-2000,0],
        )

        plot_div = plot(fig,output_type='div', include_plotlyjs=False, config= {'displaylogo': False, 
            'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})

        return JsonResponse({'plot_div': plot_div}, status = 200)

    return JsonResponse({}, status = 400)