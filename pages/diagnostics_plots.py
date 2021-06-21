from django.http import JsonResponse
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import pandas as pd
import math
import time
import json
import numpy as np
import cmocean

from env_data.models import continuous_profile, cycle_metadata, discrete_profile
from .plot_helpers import var_translation

def cmocean_to_plotly(cmap, pl_entries):
    """Function to sample cmocean colors and output list of rgb values for plotly
    cmap = color map from cmocean
    pl_entries = number of samples to take"""
    
    h = 1.0/(pl_entries-1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append('rgb'+str((C[0], C[1], C[2])))

    return pl_colorscale

def update_cohort_plot(request):
    """"""
    start = time.time()
    if request.is_ajax and request.method == "GET":

        #Get URL parameters
        year_selected = request.GET.get("year_selected", None)
        var_selected = request.GET.get("var_selected", None)

        #Build querys
        if var_selected != "NITRATE":
            query = continuous_profile.objects.filter(DEPLOYMENT__LAUNCH_DATE__year=year_selected).order_by(
                "PROFILE_ID", "PRES").values_list("DEPLOYMENT__FLOAT_SERIAL_NO","DEPLOYMENT__PLATFORM_NUMBER", 
                "PROFILE_ID", "PRES", var_selected)
            data = pd.DataFrame(query, columns=["FLOAT_SERIAL_NO","PLATFORM_NUMBER", "PROFILE_ID", "PRES", var_selected])
            
        dis_query = discrete_profile.objects.filter(DEPLOYMENT__LAUNCH_DATE__year=year_selected).order_by(
            "PROFILE_ID", "PRES").values_list("DEPLOYMENT__FLOAT_SERIAL_NO","DEPLOYMENT__PLATFORM_NUMBER", 
            "PROFILE_ID", "PRES", var_selected)
        
        print(time.time()-start, "Query build")
        start = time.time()

        #Fetch data and convert to dataframe
        #data = np.core.records.fromrecords(query, names=["DEPLOYMENT", "PROFILE_ID", "PRES", var_selected])
        dis_data = pd.DataFrame(dis_query, columns=["FLOAT_SERIAL_NO","PLATFORM_NUMBER", 
            "PROFILE_ID", "PRES", var_selected])

        print(time.time()-start, "Execute query and DFs")
        start = time.time()

        #Number of subplot rows based on number of floats
        wmos = dis_data.PLATFORM_NUMBER.unique()
        n_rows = math.ceil(len(wmos)/2)
        fig = make_subplots(rows=n_rows, cols=2)

        #each float (seperate subplot)
        for i, wmo in enumerate(wmos):
            #Current row and col of subplot
            crt_row = math.floor(i/2)+1
            crt_col = i%2+1

            #------------Continuous data -----------#
            if var_selected != "NITRATE":
                #subset to one float
                data_sub = data.loc[data.PLATFORM_NUMBER==wmo,:]
                sn = data_sub.reset_index().loc[0, "FLOAT_SERIAL_NO"]

                #continuous colormaps
                n_colors = len(data_sub.PROFILE_ID.unique())
                colors = cmocean_to_plotly(cmocean.cm.dense, n_colors)

                #Opacity values
                opacity_vals = np.logspace(np.log10(0.5), np.log10(1), n_colors) 

                #Each profile (series)
                for j, prof in enumerate(data_sub.PROFILE_ID.unique()):
                    fig.add_trace(
                        go.Scatter(
                            x=data_sub.loc[data["PROFILE_ID"]==prof, var_selected],
                            y=data_sub.loc[data["PROFILE_ID"]==prof, "PRES"]*-1,
                            mode='lines',
                            marker = {
                                'color': colors[j],
                            },
                            opacity=opacity_vals[j],
                            #customdata = hov_data,
                            hovertemplate ='%{x:.3f}',
                            name="Profile:"+prof,
                        ),
                    row=crt_row,
                    col=crt_col,
                    )

            #--------- Discrete data ------------#
            #subset to one float
            dis_data_sub = dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,:]
            sn = dis_data_sub.reset_index().loc[0, "FLOAT_SERIAL_NO"]

            #discrete colormaps
            n_colors = len(dis_data_sub.PROFILE_ID.unique())
            colors = cmocean_to_plotly(cmocean.cm.dense, n_colors)

            #Opacity values
            opacity_vals = np.logspace(np.log10(0.5), np.log10(1), n_colors) 

            #Each profile (series)
            for k, prof in enumerate(dis_data_sub.PROFILE_ID.unique()):
                fig.add_trace(
                    go.Scatter(
                        x=dis_data_sub.loc[dis_data["PROFILE_ID"]==prof, var_selected],
                        y=dis_data_sub.loc[dis_data["PROFILE_ID"]==prof, "PRES"]*-1,
                        mode='markers',
                        marker = {
                            'color': colors[k],
                        },
                        opacity=opacity_vals[k],
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Profile:"+prof,
                    ),
                row=crt_row,
                col=crt_col,
                )

            #Float Label position
            if crt_col == 1:
                xpos = 0.07
            else:
                xpos = 0.62

            #Float label
            fig.add_annotation(text="WMO: "+wmo+" SN: "+str(sn),
                xref="paper", yref="paper", xanchor='center', yanchor='bottom',
                x=xpos, y=1, showarrow=False,
                )

        # Formatting
        fig.update_layout(
            template = "ggplot2",
            yaxis = {'title':"Pressure"},
            font = {"size":12},
            height=825,
            showlegend=False,
            margin={'t': 30, 'l':0,'r':0,'b':0},
        )

        #Black border of plot
        fig.update_xaxes(title=var_translation[var_selected],
                showline=True,
                linewidth=1,
                linecolor="#000000",
                mirror=True)

        fig.update_yaxes(title="Pressure (dbar)",
                showline=True,
                linewidth=1,
                linecolor="#000000",
                mirror=True)

        #Output as html div
        plot_div = plot(fig,output_type='div', include_plotlyjs=False, config= {
            'displaylogo': False, 'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})  

        print(time.time()-start, "Plotly")
        return JsonResponse({'plot_div': plot_div}, status = 200)

    return JsonResponse({}, status = 400)


def update_cohort_latest_plot(request):
    """"""
    if request.is_ajax and request.method == "GET":

        year_selected = request.GET.get("year_selected", None)
        vars_selected = json.loads(request.GET.get("vars_selected", None))

        print(vars_selected)

        #Get list of latest profiles
        profile_ids_q = cycle_metadata.objects.filter(DEPLOYMENT__LAUNCH_DATE__year=year_selected).order_by(
            '-DEPLOYMENT__id','-PROFILE_ID').distinct('DEPLOYMENT__id').values_list("PROFILE_ID")

        #latest continuous data query
        query = continuous_profile.objects.filter(PROFILE_ID__in=profile_ids_q).order_by(
            "PROFILE_ID", "PRES").values_list("DEPLOYMENT__FLOAT_SERIAL_NO","DEPLOYMENT__PLATFORM_NUMBER", 
            "PROFILE_ID", "PRES", "PSAL","TEMP","DOXY","CHLA","BBP700","CDOM","PH_IN_SITU_TOTAL")

        #Latest discrete data query
        dis_query = discrete_profile.objects.filter(PROFILE_ID__in=profile_ids_q).order_by(
            "PROFILE_ID", "PRES").values_list("DEPLOYMENT__FLOAT_SERIAL_NO","DEPLOYMENT__PLATFORM_NUMBER", 
            "PROFILE_ID", "PRES", "PSAL","TEMP","DOXY","CHLA","BBP700","CDOM","PH_IN_SITU_TOTAL","NITRATE")

        #Cycle metadata query
        cycle_meta_query = cycle_metadata.objects.filter(PROFILE_ID__in=profile_ids_q).order_by(
            "PROFILE_ID").values_list("TimeStartProfile")
        
        #Get data and convert to dataframes
        data = pd.DataFrame(query, columns=["FLOAT_SERIAL_NO","PLATFORM_NUMBER", "PROFILE_ID", "PRES", "PSAL",
            "TEMP","DOXY","CHLA","BBP700","CDOM","PH_IN_SITU_TOTAL"])

        dis_data = pd.DataFrame(dis_query, columns=["FLOAT_SERIAL_NO","PLATFORM_NUMBER", 
            "PROFILE_ID", "PRES", "PSAL","TEMP","DOXY","CHLA","BBP700","CDOM","PH_IN_SITU_TOTAL","NITRATE"])

        wmos = data.PLATFORM_NUMBER.unique()

        #Dict to collect plots
        plot_divs={}

        #each float (seperate plot)
        for i, wmo in enumerate(wmos):
            fig = go.Figure()

            #------------------Continuous Traces-------------------
            #subset to one float
            data_sub = data.loc[data.PLATFORM_NUMBER==wmo,:]
            sn = data_sub.reset_index().loc[0, "FLOAT_SERIAL_NO"]

            #Salinity
            if vars_selected["SALck"]:
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[:, "PSAL"],
                        y=data_sub.loc[:, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': "#FEBD17",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Salinity",
                        xaxis="x"
                    ),
                )
            else: #Dummy blank trace, plotly needs an x axis trace
                fig.add_trace(
                    go.Scatter(
                        mode='lines',
                        marker = {
                            'color': "#FEBD17",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Salinity",
                        xaxis="x"
                    ),
                )


            #BBP700
            if vars_selected["BBP700ck"]:
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[:, "BBP700"],
                        y=data_sub.loc[:, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': "#80BF96",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Backscattering",
                        xaxis="x2"
                    ),
                )

            #CDOM
            if vars_selected["CDOMck"]:
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[:, "CDOM"],
                        y=data_sub.loc[:, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': "#023440",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="CDOM",
                        xaxis="x3"
                    ),
                )

            #Temeprature
            if vars_selected["TEMPck"]:
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[:, "TEMP"],
                        y=data_sub.loc[:, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': "#c9324e",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Temperature",
                        xaxis="x4"
                    ),
                )

            #DOXY
            if vars_selected["DOXYck"]:
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[:, "DOXY"],
                        y=data_sub.loc[:, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': "#1f77b4",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Dissolved Oxygen",
                        xaxis="x5"
                    ),
                )

            #pH
            if vars_selected["pHck"]:
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[:, "PH_IN_SITU_TOTAL"],
                        y=data_sub.loc[:, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': "#a8018c",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="pH In Situ Total",
                        xaxis="x7"
                    ),
                )
            #--------------------Discrete Traces ----------------------
            #subset to one float
            dis_data_sub = dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,:]
            sn = dis_data_sub.reset_index().loc[0, "FLOAT_SERIAL_NO"]

            #Salinity
            if vars_selected["SALck"]:
                fig.add_trace(
                    go.Scatter(
                        x=dis_data_sub.loc[:, "PSAL"],
                        y=dis_data_sub.loc[:, "PRES"]*-1,
                        mode='markers',
                        marker = {
                            'color': "#FEBD17",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Salinity",
                        xaxis="x"
                    ),
                )

            #BBP700
            if vars_selected["BBP700ck"]:
                fig.add_trace(
                    go.Scatter(
                        x=dis_data_sub.loc[:, "BBP700"],
                        y=dis_data_sub.loc[:, "PRES"]*-1,
                        mode='markers',
                        marker = {
                            'color': "#80BF96",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Backscattering",
                        xaxis="x2"
                    ),
                )

            #CDOM
            if vars_selected["CDOMck"]:
                fig.add_trace(
                    go.Scatter(
                        x=dis_data_sub.loc[:, "CDOM"],
                        y=dis_data_sub.loc[:, "PRES"]*-1,
                        mode='markers',
                        marker = {
                            'color': "#023440",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="CDOM",
                        xaxis="x3"
                    ),
                )

            #Temeprature
            if vars_selected["TEMPck"]:
                fig.add_trace(
                    go.Scatter(
                        x=dis_data_sub.loc[:, "TEMP"],
                        y=dis_data_sub.loc[:, "PRES"]*-1,
                        mode='markers',
                        marker = {
                            'color': "#c9324e",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Temperature",
                        xaxis="x4"
                    ),
                )

            #DOXY
            if vars_selected["DOXYck"]:
                fig.add_trace(
                    go.Scatter(
                        x=dis_data_sub.loc[:, "DOXY"],
                        y=dis_data_sub.loc[:, "PRES"]*-1,
                        mode='markers',
                        marker = {
                            'color': "#1f77b4",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Dissolved Oxygen",
                        xaxis="x5"
                    ),
                )

            #Nitrate
            if vars_selected["NITRATEck"]:
                fig.add_trace(
                    go.Scatter(
                        x=dis_data_sub.loc[:, "NITRATE"],
                        y=dis_data_sub.loc[:, "PRES"]*-1,
                        mode='markers',
                        marker = {
                            'color': "#bc925a",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Nitrate",
                        xaxis="x6"
                    ),
                )

            #pH
            if vars_selected["pHck"]:
                fig.add_trace(
                    go.Scatter(
                        x=dis_data_sub.loc[:, "PH_IN_SITU_TOTAL"],
                        y=dis_data_sub.loc[:, "PRES"]*-1,
                        mode='markers',
                        marker = {
                            'color': "#a8018c",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="pH",
                        xaxis="x7"
                    ),
                )

            fig.add_annotation(text="WMO: "+wmo+" SN: "+str(sn)+"    "+cycle_meta_query[i][0].strftime("%Y-%m-%d %H:%M"),
                xref="paper", yref="paper", xanchor='left', yanchor='bottom',
                x=0.02, y=.75, showarrow=False,
                )

            if vars_selected["SALck"]:
                fig.update_layout(
                    xaxis=dict(
                        title=dict(
                            text="Practical Salinity",
                            standoff=0,
                        ),
                        titlefont=dict(
                            color="#FEBD17"
                        ),
                        tickfont=dict(
                            color="#FEBD17"
                        ),
                        position=0.15,
                        range=[34.8, 36],
                        showline=True,
                        linewidth=1,
                        linecolor="#FEBD17"
                    )
                )
            else:
                fig.update_layout(
                    xaxis={'showgrid': False, # thin lines in the background
                        'zeroline': False, # thick line at x=0
                        'visible': False} # numbers below
                )         

            # Formatting
            fig.update_layout(
                template = "ggplot2",
                #yaxis = {'title':"Pressure"},
                font = {"size":12},
                height=825,
                showlegend=False,
                margin={'t': 0, 'l':0,'r':0,'b':0},
                yaxis=dict(
                    domain=[0.15, 0.78],
                    showline=True,
                    linewidth=1,
                    linecolor="#000000",
                    mirror=True
                ),
                xaxis2=dict(
                    title=dict(
                        text="Particle Backscattering at 700 nm (m<sup>-1</sup>)",
                        standoff=0,
                    ),
                    titlefont=dict(
                        color="#80BF96"
                    ),
                    tickfont=dict(
                        color="#80BF96"
                    ),
                    anchor="free",
                    overlaying="x",
                    side="bottom",
                    position=0.08,
                    range=[0, .001],
                    showline=True,
                    linewidth=1,
                    linecolor="#80BF96",
                    showgrid=False
                ),
                xaxis3=dict(
                    title=dict(
                        text="Coloured Dissolved Organic Matter (ppb)",
                        standoff=10,
                    ),
                    titlefont=dict(
                        color="#023440"
                    ),
                    tickfont=dict(
                        color="#023440"
                    ),
                    anchor="free",
                    overlaying="x",
                    side="bottom",
                    position=0.0,
                    range=[0, 3],
                    showline=True,
                    linewidth=1,
                    linecolor="#023440",
                    showgrid=False
                ),
                xaxis4=dict(
                    title=dict(
                        text="In-situ Temperature (°C)",
                        standoff=0,
                    ),
                    titlefont=dict(
                        color="#c9324e"
                    ),
                    tickfont=dict(
                        color="#c9324e"
                    ),
                    anchor="free",
                    overlaying="x",
                    side="top",
                    position=.78,
                    range=[0, 15],
                    showline=True,
                    linewidth=1,
                    linecolor="#c9324e",
                    showgrid=False
                ),
                xaxis5=dict(
                    title=dict(
                        text="Dissolved Oxygen (μmol/kg)",
                        standoff=0,
                    ),
                    titlefont=dict(
                        color="#1f77b4"
                    ),
                    tickfont=dict(
                        color="#1f77b4"
                    ),
                    anchor="free",
                    overlaying="x",
                    side="top",
                    position=.85,
                    range=[150, 300],
                    showline=True,
                    linewidth=1,
                    linecolor="#1f77b4",
                    showgrid=False
                ),
                xaxis6=dict(
                    title=dict(
                        text="Nitrate (μmol/kg)",
                        standoff=0,
                    ),
                    titlefont=dict(
                        color="#bc925a"
                    ),
                    tickfont=dict(
                        color="#bc925a"
                    ),
                    anchor="free",
                    overlaying="x",
                    side="top",
                    position=.92,
                    range=[0, 25],
                    showline=True,
                    linewidth=1,
                    linecolor="#bc925a",
                    showgrid=False
                ),
                xaxis7=dict(
                    title=dict(
                        text="In-situ pH (total)",
                        standoff=10,
                    ),
                    titlefont=dict(
                        color="#a8018c"
                    ),
                    tickfont=dict(
                        color="#a8018c"
                    ),
                    anchor="free",
                    overlaying="x",
                    side="top",
                    position=1,
                    #range=[0, 25],
                    showline=True,
                    linewidth=1,
                    linecolor="#a8018c",
                    showgrid=False
                ),
            )

            plot_divs["plot_div"+str(i)] = plot(fig,output_type='div', include_plotlyjs=False, config= {
                'displaylogo': False, 'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})  

        return JsonResponse(plot_divs, status = 200)

    return JsonResponse({}, status = 400)