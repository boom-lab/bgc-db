import plotly.graph_objs as go
from plotly.offline import plot
import time
import numpy as np
import pandas as pd

from env_data.models import cycle_metadata

def volts_plot(filters):
    start = time.time()

    query = cycle_metadata.objects.filter(**filters).order_by("ProfileId").values_list("ProfileId","QuiescentVolts",
        "Sbe41cpVolts","AirPumpVolts","BuoyancyPumpVolts","Sbe63Volts","McomsVolts","GpsFixDate")
    data = np.core.records.fromrecords(query, names=["ProfileId","QuiescentVolts","Sbe41cpVolts","AirPumpVolts",
        "BuoyancyPumpVolts","Sbe63Volts","McomsVolts","GpsFixDate"])

    hov = pd.DataFrame()
    hov["GpsFixDate"] = data["GpsFixDate"]
    hov["GpsFixDate"] = hov.GpsFixDate.dt.strftime('%Y-%m-%d')
    hov_data = hov.values.tolist()

    fig = go.Figure()

    #Quiescent Volts
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["QuiescentVolts"],
            mode='lines',
            marker = {
                'color': "#BABDBF",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            name="Quiescent Volts"
        ),
    )

    #Air Pump
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["AirPumpVolts"],
            mode='lines',
            marker = {
                'color': "#3C7373",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            #yaxis="y2",
            name="Air Pump"
        ),
    )
    
    #SBE 41Cp
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["Sbe41cpVolts"],
            mode='lines',
            marker = {
                'color': "#e53232",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            #yaxis="y2",
            name="SBE41cp - CTD"
        ),
    )

    #Buoyancy Pump Volts
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["BuoyancyPumpVolts"],
            mode='lines',
            marker = {
                'color': "#592316",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            #yaxis="y2",
            name="Buoyancy Pump"
        ),
    )

    #SBE63
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["Sbe63Volts"],
            mode='lines',
            marker = {
                'color': "#ff7f0e",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            #yaxis="y2",
            name="SBE63 - DOXY"
        ),
    )

    
    #MCOMS
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["McomsVolts"],
            mode='lines',
            marker = {
                'color': "#1f77b4",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            #yaxis="y2",
            name="MCOMS"
        ),
    )

    # Formatting
    fig.update_layout(
        template = "ggplot2",
        #title = "Battery",
        xaxis = {'title':"Cycle"},
        yaxis = {'title':"Voltage"},
        font = {"size":15},
        height=500,
        showlegend=True,
        margin={'t': 30, 'l':0,'r':0,'b':0},
        yaxis_range=[8,12]
    )

    plot_div = plot(fig,output_type='div', include_plotlyjs=False, config= {
        'displaylogo': False, 'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})  
    end = time.time()
    print("elapsed:", end-start)
    return plot_div

def amps_plot(filters):

    query = cycle_metadata.objects.filter(**filters).order_by("ProfileId").values_list("ProfileId","QuiescentAmps","Sbe41cpAmps",
        "AirPumpAmps","BuoyancyPumpAmps","Sbe63Amps","McomsAmps","GpsFixDate")
    data = np.core.records.fromrecords(query, names=["ProfileId","QuiescentAmps","Sbe41cpAmps","AirPumpAmps","BuoyancyPumpAmps",
        "Sbe63Amps","McomsAmps","GpsFixDate"])

    hov = pd.DataFrame()
    hov["GpsFixDate"] = data["GpsFixDate"]
    hov["GpsFixDate"] = hov.GpsFixDate.dt.strftime('%Y-%m-%d')
    hov_data = hov.values.tolist()

    fig = go.Figure()
    #Quiescent Amps
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["QuiescentAmps"],
            mode='lines',
            marker = {
                'color': "#BABDBF",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            name="Quiescent Amps"
        ),
    )

    #Air Pump
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["AirPumpAmps"],
            mode='lines',
            marker = {
                'color': "#3C7373",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            #yaxis="y2",
            name="Air Pump"
        ),
    )
    
    #SBE 41Cp
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["Sbe41cpAmps"],
            mode='lines',
            marker = {
                'color': "#e53232",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            #yaxis="y2",
            name="SBE41cp - CTD"
        ),
    )

    #Buoyancy Pump Amps
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["BuoyancyPumpAmps"],
            mode='lines',
            marker = {
                'color': "#592316",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            #yaxis="y2",
            name="Buoyancy Pump"
        ),
    )

    #SBE63
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["Sbe63Amps"],
            mode='lines',
            marker = {
                'color': "#ff7f0e",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            #yaxis="y2",
            name="SBE63 - DOXY"
        ),
    )

    
    #MCOMS
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["McomsAmps"],
            mode='lines',
            marker = {
                'color': "#1f77b4",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            #yaxis="y2",
            name="MCOMS"
        ),
    )

    # Formatting
    fig.update_layout(
        template = "ggplot2",
        #title = "Amps",
        xaxis = {'title':"Cycle"},
        yaxis = {'title':"Amps"},
        font = {"size":15},
        height=500,
        showlegend=True,
        margin={'t': 30, 'l':0,'r':0,'b':0},
        yaxis_range=[0,.8]
    )

    plot_div = plot(fig,output_type='div', include_plotlyjs=False, config= {
        'displaylogo': False, 'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})
    return plot_div

def buoyancy_position_plot(filters):

    query = cycle_metadata.objects.filter(**filters).order_by("ProfileId").values_list("ProfileId","CurrentBuoyancyPosition",
        "DeepProfileBuoyancyPosition","ParkBuoyancyPosition","SurfaceBuoyancyPosition","GpsFixDate")
    data = np.core.records.fromrecords(query, names=["ProfileId","CurrentBuoyancyPosition",
        "DeepProfileBuoyancyPosition","ParkBuoyancyPosition","SurfaceBuoyancyPosition","GpsFixDate"])

    hov = pd.DataFrame()
    hov["GpsFixDate"] = data["GpsFixDate"]
    hov["GpsFixDate"] = hov.GpsFixDate.dt.strftime('%Y-%m-%d')
    hov_data = hov.values.tolist()

    fig = go.Figure()

    #Current Buoyancy Position
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["CurrentBuoyancyPosition"],
            mode='lines',
            marker = {
                'color': "#80B2F2",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            name="Current Buoyancy Position"
        ),
    )

    #Deep Profile Buoyancy Position
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["DeepProfileBuoyancyPosition"],
            mode='lines',
            marker = {
                'color': "#BFB7A8",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            name="Deep Profile Buoyancy Position"
        ),
    )

    #Park Buoyancy Position
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["ParkBuoyancyPosition"],
            mode='lines',
            marker = {
                'color': "#BF5454",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            name="Park Buoyancy Position"
        ),
    )

    #Surface Buoyancy Position
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data["SurfaceBuoyancyPosition"],
            mode='lines',
            marker = {
                'color': "#733838",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            name="Surface Buoyancy Position"
        ),
    )


    # Formatting
    fig.update_layout(
        template = "ggplot2",
        #title = "Amps",
        xaxis = {'title':"Cycle"},
        yaxis = {'title':"Position (counts)"},
        font = {"size":15},
        height=500,
        showlegend=True,
        margin={'t': 30, 'l':0,'r':0,'b':0},
        #yaxis_range=[0,.8]
    )

    plot_div = plot(fig,output_type='div', include_plotlyjs=False, config= {
        'displaylogo': False, 'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})  
    return plot_div

def single_var_plot(filters, var, y_label, legend_label, y_range=None):
    """
    filters: dictionary, contains filters to get to desired cycle metadata objecsts (one float)
    var: string, field name of desired variable
    y_label: string, label for y axis
    legend_label: string, label for legend and series
    y_axis_range: optional, 2 element list, ex. [0,10] is minimum of 0 max of 10. If let out it is autoscalled.
    """

    query = cycle_metadata.objects.filter(**filters).order_by("ProfileId").values_list("ProfileId",var,"GpsFixDate")
    data = np.core.records.fromrecords(query, names=["ProfileId",var,"GpsFixDate"])

    hov = pd.DataFrame()
    hov["GpsFixDate"] = data["GpsFixDate"]
    hov["GpsFixDate"] = hov.GpsFixDate.dt.strftime('%Y-%m-%d')
    hov_data = hov.values.tolist()

    fig = go.Figure()

    #Air Bladder Pressure
    fig.add_trace(
        go.Scatter(
            x=data["ProfileId"],
            y=data[var],
            mode='lines',
            marker = {
                'color': "#80B2F2",
            },
            customdata = hov_data,
            hovertemplate ='%{y:.2f}<br>%{customdata[0]}',
            name=legend_label
        ),
    )

    # Formatting
    fig.update_layout(
        template = "ggplot2",
        xaxis = {'title':"Cycle"},
        yaxis = {'title':y_label},
        font = {"size":15},
        height=500,
        showlegend=True,
        margin={'t': 30, 'l':0,'r':0,'b':0},
        #yaxis_range=[0,.8]
    )

    if y_range:
        fig.update_layout(
            yaxis_range=y_range
        )

    plot_div = plot(fig,output_type='div', include_plotlyjs=False, config= {
        'displaylogo': False, 'modeBarButtonsToRemove':['lasso2d', 'select2d','resetScale2d']})  
    return plot_div