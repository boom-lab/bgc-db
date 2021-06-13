import plotly.graph_objs as go

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
    "CDOM":"Coloured dissolved organic matter (ppb)"
}