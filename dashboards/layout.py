import dash_html_components as html
import dash_core_components as dcc
from datetime import date

#Layout
layout = html.Div([html.H1('BGC Argo'),
    html.Div([
        #Data selection
        html.Div([
            #Date filter

            html.Label('Date'),
            dcc.DatePickerRange(
                id='date_filter',
                initial_visible_month=date.today(),
                end_date=date.today(),
                className='date_picker'
            ),

            #Float / Profile selection
            html.Label('Float ID / Profile'),
            dcc.Dropdown(
                id='filter',
                value=[],
                multi=True
            ),
        ],
        className="pretty_container data_selector"),

        #Environmental Plot Selections
        html.Div([
            #bottom axis selection
            html.Label('Bottom Axis'),
            dcc.Dropdown(
                id='bvar',
                options=['TEMP','PRES','PSAL'],
                value='TEMP'
            ),

            #top axis selection
            html.Label('Top Axis'),
            dcc.Dropdown(
                id='tvar',
                options=['TEMP','PRES','PSAL'],
                value=None
            ),

            #Y axis selection
            html.Label('Y Axis'),
            dcc.Dropdown(
                id='yvar',
                options=['TEMP','PRES','PSAL'],
                value='z'
            )
        ],className="pretty_container plot_controls", id="plot_controls"),


        #Tabs
        html.Div([
            dcc.Tabs(
                parent_className='custom-tabs',
                className='custom-tabs-container',
                id='custom-tabs',
                children=[
                    dcc.Tab(label='Plot',
                        className='custom-tab',
                        selected_className='custom-tab--selected',
                        children= [dcc.Graph(id='feature-graphic', className='plot')]
                    )
                ]
            )
        ], className="pretty_container plot_app"),



    ], className="container")
])