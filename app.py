
################################################################################
###
### Libraries
###
################################################################################
import dash

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from assets.servo_control import servo_manager


################################################################################
###
### Setup
###
################################################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, 'criddyp.css', 'custom.css'], title='servo GUI', update_title=None)
# app.config.suppress_callback_exceptions = True

sm = servo_manager()


################################################################################
###
### Layout
###
################################################################################
app.layout =  html.Div([

    dbc.Row(
        [
            # gauge to show current position
            dbc.Col(
                [
                    dcc.Graph(id='fig', figure=sm.get_fig())
                ],
            ),        
        ],
    ),

    dbc.Row(
        [
            
            # return to zero
            dbc.Col(
                [
                    dcc.Slider(id='slider-drag', min=-90, max=90, value=0, updatemode='drag'),
                    # daq.Slider(
                    #     min=-90,
                    #     max=90,
                    #     value=0,
                    #     handleLabel={"showCurrentValue": True,"label": "Angle"},
                    #     step=10,
                    #     id='slider-drag',
                    # ),
                    html.Div(id='slider-drag-output', style={'margin-top': 5, 'color':'white'}),

                    dbc.Button('Return to zero', id='b_ret_zero', className='center'),
                ],                
            ),
        ],
    ),

    # interval
    dcc.Interval(
        id='interval',
        interval=50, # in milliseconds
        n_intervals=0
    )

],className='body',)

################################################################################
###
### Callbacks
###
################################################################################
# slider
@app.callback(
    Output('slider-drag-output', 'children'),
    Input('slider-drag', 'value')
)
def display_value(value):
    global sm
    sm.move_servo(value)
    return ''

# return to zero
@app.callback(
    Output('slider-drag', 'value'),
    Input(component_id='b_ret_zero', component_property='n_clicks')
)
def ret_zero(n):
    global sm
    triggered = [p['prop_id'].split('.')[0] for p in dash.callback_context.triggered]
    if 'b_ret_zero' in triggered:
        sm.goto_zero()
    return 0
        

# update grapic
@app.callback(
    Output(component_id='fig', component_property='figure'),
    Input(component_id='interval', component_property='n_intervals'),
)
def update_fig(n):
    global sm
    return sm.get_fig()


################################################################################
###
### Run
###
################################################################################
if __name__ == '__main__':
    app.run_server(debug=True, port=8080, host='169.254.228.85')