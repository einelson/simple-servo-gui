
################################################################################
###
### Libraries
###
################################################################################
import dash

import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import html
import dash_daq as daq
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

            # clockwise button
            dbc.Col(
                [
                    # dbc.Button('Clockwise', id='b_spin_counter', className='center'),
                    daq.Joystick(
                        id='servo_control',
                        label="Servo controller",
                        angle=0,
                        size=250,
                        style={'color':'white'},
                    ),
                    html.Div(id='ret_spin', style={'color':'white'},),

                ],
            ),            
        ],
    ),

    dbc.Row(
        [
            # return to zero
            dbc.Col(
                [
                    dbc.Button('Return to zero', id='b_ret_zero', className='centered'),
                    html.Div(id='ret_ret_zero'),
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

# counter clockwise
@app.callback(
    Output(component_id='ret_spin', component_property='children'),
    Input(component_id='servo_control', component_property='angle'),
)
def spin_counter(angle):
    global sm
    sm.move_servo()
    return angle

# return to zero
@app.callback(
    Output(component_id='ret_ret_zero', component_property='children'),
    Input(component_id='b_ret_zero', component_property='n_clicks')
)
def ret_zero(n):
    global sm
    triggered = [p['prop_id'].split('.')[0] for p in dash.callback_context.triggered]
    if 'b_ret_zero' in triggered:
        print('goto zero')
        sm.goto_zero()
        

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