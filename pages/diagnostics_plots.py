from django.http import JsonResponse
import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd
import json
import cmocean

from env_data.models import continuous_profile, cycle_metadata, discrete_profile
from .plot_helpers import var_translation, var_ranges, cmocean_to_plotly_simple

def update_compare_latest_profiles(request):
    if request.is_ajax and request.method == "GET":
        # get the selections
        deployments = request.GET.getlist("deployments[]", None)
        var_selected = request.GET.get("var_selected", None)

        #Get list of latest profiles
        profile_ids_q = cycle_metadata.objects.filter(DEPLOYMENT__PLATFORM_NUMBER__in=deployments).order_by(
            '-DEPLOYMENT__id','-PROFILE_ID').distinct('DEPLOYMENT__id').values_list("PROFILE_ID")

        #latest continuous data query
        if var_selected not in ["NITRATE","VK_PH","IB_PH","IK_PH"]:
            con_query = continuous_profile.objects.filter(PROFILE_ID__in=profile_ids_q).order_by(
                "PROFILE_ID", "PRES").values_list("DEPLOYMENT__FLOAT_SERIAL_NO","DEPLOYMENT__PLATFORM_NUMBER", 
                "PROFILE_ID", "PRES", var_selected)
                
            con_data = pd.DataFrame(con_query, columns=["FLOAT_SERIAL_NO","PLATFORM_NUMBER", "PROFILE_ID", "PRES", var_selected])

        #Latest discrete data query
        dis_query = discrete_profile.objects.filter(PROFILE_ID__in=profile_ids_q).order_by(
            "PROFILE_ID", "PRES").values_list("DEPLOYMENT__FLOAT_SERIAL_NO","DEPLOYMENT__PLATFORM_NUMBER", 
            "PROFILE_ID", "PRES", var_selected)

        dis_data = pd.DataFrame(dis_query, columns=["FLOAT_SERIAL_NO","PLATFORM_NUMBER", "PROFILE_ID", "PRES", var_selected])

        wmos = dis_data.PLATFORM_NUMBER.unique()

        #Colors
        colors = cmocean_to_plotly_simple(cmocean.cm.phase,len(wmos))

        fig = go.Figure()

        #each float (seperate plot)
        for i, wmo in enumerate(wmos):

            #------------------Continuous Traces-------------------#
            if var_selected not in ["NITRATE","VK_PH","IB_PH","IK_PH"]:
                #subset to one float
                data_sub = con_data.loc[con_data.PLATFORM_NUMBER==wmo,:]
                sn = data_sub.reset_index().loc[0, "FLOAT_SERIAL_NO"]

                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[:, var_selected],
                        y=data_sub.loc[:, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': colors[i],
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f} <br>%{y:.0f}',
                        name="SN: "+sn,
                        xaxis="x"
                    ),
                )

            #---------------Discrete Traces----------------------#
            dis_data_sub = dis_data.loc[dis_data.PLATFORM_NUMBER==wmo,:]
            sn = dis_data_sub.reset_index().loc[0, "FLOAT_SERIAL_NO"]

            fig.add_trace(
                go.Scatter(
                    x=dis_data_sub.loc[:, var_selected],
                    y=dis_data_sub.loc[:, "PRES"]*-1,
                    mode='markers',
                    marker = {
                         'color': colors[i],
                    },
                    #customdata = hov_data,
                    hovertemplate ='%{x:.3f} <br>%{y:.0f}',
                    name="SN: "+sn,
                    xaxis="x"
                ),
            )
            # ---------------Formatting--------------------------#
            fig.update_layout(
                template = "ggplot2",
                xaxis = dict(
                    title=var_translation[var_selected],
                    showline=True,
                    linewidth=1,
                    linecolor="#000000",
                    mirror=True,
                    range=var_ranges[var_selected]
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
                showlegend=False,
                margin={'t': 0, 'l':0,'r':0,'b':0},
                yaxis_range=[-2000,0],
            )

        plot_div = plot(fig,output_type='div', include_plotlyjs=False, config= {
            'displaylogo': False, 'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})  

        return JsonResponse(plot_div, status = 200, safe=False)

    return JsonResponse({}, status = 400)

def update_latest_profiles_plots(request):
    """"""
    if request.is_ajax and request.method == "GET":

        year_selected = request.GET.get("year_selected", None)
        vars_selected = json.loads(request.GET.get("vars_selected", None))

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
                            'color': "#343c91",
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

            #CHLA
            if vars_selected["CHLAck"]:
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[:, "CHLA"],
                        y=data_sub.loc[:, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': "#43b53b",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Chlorophyll",
                        xaxis="x8"
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
                            'color': "#343c91",
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

            #CHLA
            if vars_selected["CHLAck"]:
                fig.add_trace(
                    go.Scatter(
                        x=dis_data_sub.loc[:, "CHLA"],
                        y=dis_data_sub.loc[:, "PRES"]*-1,
                        mode='markers',
                        marker = {
                            'color': "#43b53b",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Backscattering",
                        xaxis="x8"
                    ),
                )

            #Float ID text
            fig.add_annotation(text="WMO: "+wmo+" SN: "+str(sn)+"    "+cycle_meta_query[i][0].strftime("%Y-%m-%d %H:%M"),
                xref="paper", yref="paper", xanchor='left', yanchor='bottom',
                x=0.02, y=.75, showarrow=False,
                )

            #Axis formatting
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
                        position=0.20,
                        range=var_ranges["PSAL"],
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
                    domain=[0.20, 0.78],
                    showline=True,
                    linewidth=1,
                    linecolor="#000000",
                    mirror=True,
                    range=[-2000,0]
                ),
                xaxis2=dict(
                    title=dict(
                        text="Particle Backscattering at 700 nm (m<sup>-1</sup>)",
                        standoff=0,
                    ),
                    titlefont=dict(
                        color="#343c91"
                    ),
                    tickfont=dict(
                        color="#343c91"
                    ),
                    anchor="free",
                    overlaying="x",
                    side="bottom",
                    position=0.14,
                    range=var_ranges["BBP700"],
                    showline=True,
                    linewidth=1,
                    linecolor="#343c91",
                    showgrid=False
                ),
                xaxis3=dict(
                    title=dict(
                        text="Coloured Dissolved Organic Matter (ppb)",
                        standoff=0,
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
                    position=0.07,
                    range=var_ranges["CDOM"],
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
                    range=var_ranges["TEMP"],
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
                    range=var_ranges["DOXY"],
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
                    range=var_ranges["NITRATE"],
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
                    range=var_ranges["PH_IN_SITU_TOTAL"],
                    showline=True,
                    linewidth=1,
                    linecolor="#a8018c",
                    showgrid=False
                ),
                xaxis8=dict(
                    title=dict(
                        text="Chlorophyll a (mg/m<sup>3</sup>)",
                        standoff=10,
                    ),
                    titlefont=dict(
                        color="#43b53b"
                    ),
                    tickfont=dict(
                        color="#43b53b"
                    ),
                    anchor="free",
                    overlaying="x",
                    side="bottom",
                    position=0.0,
                    range=var_ranges["CHLA"],
                    showline=True,
                    linewidth=1,
                    linecolor="#43b53b",
                    showgrid=False
                ),
            )

            plot_divs["plot_div"+str(i)] = plot(fig,output_type='div', include_plotlyjs=False, config= {
                'displaylogo': False, 'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})  

        return JsonResponse(plot_divs, status = 200)

    return JsonResponse({}, status = 400)