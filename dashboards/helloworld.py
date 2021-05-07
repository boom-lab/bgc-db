import dash
import dash_core_components as dcc
import dash_html_components as html
from dashboards.layout import layout
from dash.dependencies import Output, Input
from django_plotly_dash import DjangoDash

app = DjangoDash('SimpleExample')

app.layout = layout

@app.callback(
        Output('feature-graphic', 'figure'),
        [Input('filter', 'value'),
        Input('bvar', 'value'),
        Input('yvar', 'value'),
        Input('tvar', 'value'),
        ])
def update_graph(filters, bvar, yvar, tvar):
    sub = data.loc[data.selector.isin(filters),:]

    fig = go.Figure()

    #Add bottom axis traces
    for filt in filters:
        sub = data.loc[data.selector == filt,:]
        hov_data = np.stack((sub['WMO'], sub['ProfileId'], sub['TimeStartProfile_str'], sub['gps_lat'], sub['gps_lon'] ),axis = -1) #Hover data
        add_bottom_trace(fig, sub, hov_data, bvar, yvar) #add trace

    #Add top axis traces - only display if selected
    if tvar:
        for filt in filters:
            sub = data.loc[data.selector == filt,:]
            hov_data = np.stack((sub['WMO'], sub['ProfileId'], sub['TimeStartProfile_str'], sub['gps_lat'], sub['gps_lon'] ),axis = -1)
            add_top_trace(fig, sub, hov_data, tvar, yvar)


        #Top axis formatting
        fig.update_layout(
            xaxis2=dict(
                title=env_vars_formats[tvar],
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
            )
        )

    # Formatting
    fig.update_layout(
        template = "seaborn",
        xaxis = {'title':env_vars_formats[bvar]},
        yaxis = {'title':env_vars_formats[yvar]},
        font = {"size":15},
        #title = "test 3",
        #title_x = .065,

    )

    return fig

def add_bottom_trace(fig, data, hov_data, bvar, yvar):
    # Bottom x axis trace
    fig.add_trace(
        go.Scatter(
            x=data[bvar],
            y=data[yvar],
            mode='lines',
            marker = {
                'size':8,
                'color': '#000000',
                'symbol':'circle',
                'line':{'width':0}
            },
            customdata = hov_data,
            hovertemplate ='Float ID: %{customdata[0]}<br>Profile: %{customdata[1]}<br>Profile Start: %{customdata[2]}<br>Lat: %{customdata[3]}<br>Long: %{customdata[4]}',
            #name='bottom x',
            xaxis="x"
        ),
    )


def add_top_trace(fig, data, hov_data, tvar, yvar):
    fig.add_trace(
        go.Scatter(
            x=data[tvar],
            y=data[yvar],
            mode='lines',
            marker = {
                'size':8,
                'color': "#9467bd",
                'symbol':'circle',
                'line':{'width':0}
            },
            customdata = hov_data,
            hovertemplate ='Float ID: %{customdata[0]}<br>Profile: %{customdata[1]}<br>Profile Start: %{customdata[2]}<br>Lat: %{customdata[3]}<br>Long: %{customdata[4]}',
            #name='top x',
            xaxis="x2"
        ),
    )