from django.http import JsonResponse
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import math

from env_data.models import continuous_profile, cycle_metadata

def update_cohort_plot(request):
    """"""
    if request.is_ajax and request.method == "GET":

        year_selected = request.GET.get("year_selected", None)
        var_selected = request.GET.get("var_selected", None)

        query = continuous_profile.objects.filter(DEPLOYMENT__LAUNCH_DATE__year=year_selected).order_by(
            "PROFILE_ID", "PRES").values_list("DEPLOYMENT__FLOAT_SERIAL_NO","DEPLOYMENT__PLATFORM_NUMBER", 
            "PROFILE_ID", "PRES", var_selected)
        
        #data = np.core.records.fromrecords(query, names=["DEPLOYMENT", "PROFILE_ID", "PRES", var_selected])
        data = pd.DataFrame(query, columns=["FLOAT_SERIAL_NO","PLATFORM_NUMBER", "PROFILE_ID", "PRES", var_selected])
        
        #Number of subplot rows based on number of floats
        wmos = data.PLATFORM_NUMBER.unique()
        n_rows = math.ceil(len(wmos)/2)
        fig = make_subplots(rows=n_rows, cols=2)

        #each float (seperate subplot)
        for i, wmo in enumerate(wmos):
            #Current row and col of subplot
            crt_row = math.floor(i/2)+1
            crt_col = i%2+1

            #subset to one float
            data_sub = data.loc[data.PLATFORM_NUMBER==wmo,:]
            sn = data_sub.reset_index().loc[0, "FLOAT_SERIAL_NO"]

            #Each profile (series)
            for prof in data.PROFILE_ID.unique():
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[data["PROFILE_ID"]==prof, var_selected],
                        y=data_sub.loc[data["PROFILE_ID"]==prof, "PRES"]*-1,
                        mode='lines',
                        # marker = {
                        #     'color': "#1f77b4",
                        # },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Profile:"+prof,
                    ),
                row=crt_row,
                col=crt_col,
                )

            #Float Label
            if crt_col == 1:
                xpos = 0.07
            else:
                xpos = 0.62

            fig.add_annotation(text="WMO: "+wmo+" SN: "+str(sn),
                xref="paper", yref="paper", xanchor='center', yanchor='bottom',
                x=xpos, y=1, showarrow=False,
                )

        # Formatting
        fig.update_layout(
            template = "ggplot2",
            xaxis = {'title':var_selected},
            yaxis = {'title':"Pressure"},
            font = {"size":15},
            height=900,
            showlegend=False,
            margin={'t': 30, 'l':0,'r':0,'b':0},
        )



        plot_div = plot(fig,output_type='div', include_plotlyjs=False, config= {
            'displaylogo': False, 'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})  

        return JsonResponse({'plot_div': plot_div}, status = 200)

    return JsonResponse({}, status = 400)


def update_cohort_latest_plot(request):
    """"""
    if request.is_ajax and request.method == "GET":

        year_selected = request.GET.get("year_selected", None)

        #Get list of latest profiles
        profile_ids_q = cycle_metadata.objects.filter(DEPLOYMENT__LAUNCH_DATE__year=year_selected).order_by(
            '-DEPLOYMENT__id','-PROFILE_ID').distinct('DEPLOYMENT__id').values_list("PROFILE_ID")

        #Get latest continuous data
        query = continuous_profile.objects.filter(PROFILE_ID__in=profile_ids_q).order_by(
            "PROFILE_ID", "PRES").values_list("DEPLOYMENT__FLOAT_SERIAL_NO","DEPLOYMENT__PLATFORM_NUMBER", 
            "PROFILE_ID", "PRES", "PSAL","TEMP","DOXY","CHLA","BBP700","CDOM","PH_IN_SITU_TOTAL")
        
        data = pd.DataFrame(query, columns=["FLOAT_SERIAL_NO","PLATFORM_NUMBER", "PROFILE_ID", "PRES", "PSAL",
            "TEMP","DOXY","CHLA","BBP700","CDOM","PH_IN_SITU_TOTAL"])

        #Number of subplot rows based on number of floats
        wmos = data.PLATFORM_NUMBER.unique()
        n_rows = math.ceil(len(wmos)/2)

        #each float (seperate subplot)
        for i, wmo in enumerate(wmos):
            fig = go.Figure()

            #Current row and col of subplot
            crt_row = math.floor(i/2)+1
            crt_col = i%2+1

            #subset to one float
            data_sub = data.loc[data.PLATFORM_NUMBER==wmo,:]
            sn = data_sub.reset_index().loc[0, "FLOAT_SERIAL_NO"]

            #Each profile (series)
            for prof in data.PROFILE_ID.unique():
                #Salinity
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[data["PROFILE_ID"]==prof, "PSAL"],
                        y=data_sub.loc[data["PROFILE_ID"]==prof, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': "#FEBD17",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Profile:"+prof,
                        xaxis="x"
                    ),
                )

                #BBP700
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[data["PROFILE_ID"]==prof, "BBP700"],
                        y=data_sub.loc[data["PROFILE_ID"]==prof, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': "#80BF96",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Profile:"+prof,
                        xaxis="x2"
                    ),
                )

                #CDOM
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[data["PROFILE_ID"]==prof, "CDOM"],
                        y=data_sub.loc[data["PROFILE_ID"]==prof, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': "#023440",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Profile:"+prof,
                        xaxis="x3"
                    ),
                )

                #Temeprature
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[data["PROFILE_ID"]==prof, "TEMP"],
                        y=data_sub.loc[data["PROFILE_ID"]==prof, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': "#0D6973",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Profile:"+prof,
                        xaxis="x4"
                    ),
                )

                #DOXY
                fig.add_trace(
                    go.Scatter(
                        x=data_sub.loc[data["PROFILE_ID"]==prof, "DOXY"],
                        y=data_sub.loc[data["PROFILE_ID"]==prof, "PRES"]*-1,
                        mode='lines',
                        marker = {
                            'color': "#1f77b4",
                        },
                        #customdata = hov_data,
                        hovertemplate ='%{x:.3f}',
                        name="Profile:"+prof,
                        xaxis="x5"
                    ),
                )


            # #Float Label
            # if crt_col == 1:
            #     xpos = 0.07
            # else:
            #     xpos = 0.62

            # fig.add_annotation(text="WMO: "+wmo+" SN: "+str(sn),
            #     xref="paper", yref="paper", xanchor='center', yanchor='bottom',
            #     x=xpos, y=1, showarrow=False,
            #     )

        # Formatting
        fig.update_layout(
            template = "ggplot2",
            #yaxis = {'title':"Pressure"},
            font = {"size":15},
            height=900,
            showlegend=False,
            margin={'t': 30, 'l':0,'r':0,'b':0},
            yaxis=dict(
                domain=[0.15, 0.85]
            ),
            xaxis=dict(
                title="PSAL",
                titlefont=dict(
                    color="#FEBD17"
                ),
                tickfont=dict(
                    color="#FEBD17"
                ),
                position=0.15,
                range=[35, 36]
            ),
            xaxis2=dict(
                title="BBP700",
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
                range=[0, .001]
            ),
            xaxis3=dict(
                title="CDOM",
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
                range=[0, 3]
            ),
            xaxis4=dict(
                title="Temperature (C)",
                titlefont=dict(
                    color="#0D6973"
                ),
                tickfont=dict(
                    color="#0D6973"
                ),
                anchor="free",
                overlaying="x",
                side="top",
                position=.85,
                range=[0, 15]
            ),
            xaxis5=dict(
                title="Oxygen",
                titlefont=dict(
                    color="#1f77b4"
                ),
                tickfont=dict(
                    color="#1f77b4"
                ),
                anchor="free",
                overlaying="x",
                side="top",
                position=.95,
                range=[150, 300]
            ),
        )

        plot_div = plot(fig,output_type='div', include_plotlyjs=False, config= {
            'displaylogo': False, 'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})  

        return JsonResponse({'plot_div': plot_div}, status = 200)

    return JsonResponse({}, status = 400)