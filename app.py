
################################################################################
###
### Libraries
###
################################################################################
import dash

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
# import plotly.graph_objects as go
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
            # counter clockwise
            dbc.Col(
                [
                    dbc.Button('Counter Clockwise', id='b_spin_clock', className='center'),
                    html.Div(id='ret_spin_clock'),
                ],
            ),

            # gauge to show current position
            dbc.Col(
                [
                    dcc.Graph(id='fig', figure=sm.get_fig())
                ],
            ),

            # clockwise button
            dbc.Col(
                [
                    dbc.Button('Clockwise', id='b_spin_counter', className='center'),
                    html.Div(id='ret_spin_counter'),

                ],
            ),            
        ],
    ),

    dbc.Row(
        [
            # zero
            dbc.Col(
                [
                    dbc.Button('Set current angle to zero', id='b_zero_angle', className='center'),
                    html.Div(id='ret_zero_angle'),
                ]
            ),

            # return to zero
            dbc.Col(
                [
                    dbc.Button('Return to zero', id='b_ret_zero', className='center'),
                    html.Div(id='ret_ret_zero'),
                ],                
            ),
        ],
    ),

    # interval
    dcc.Interval(
        id='interval',
        interval=500, # in milliseconds
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
    Output(component_id='ret_spin_counter', component_property='children'),
    Input(component_id='b_spin_counter', component_property='n_clicks'),
)
def spin_counter(n):
    global sm
    triggered = [p['prop_id'].split('.')[0] for p in dash.callback_context.triggered]
    if 'b_spin_counter' in triggered:
        print('ccw')
        sm.move_servo('ccw')
    return ''

# clockwise
@app.callback(
    Output(component_id='ret_spin_clock', component_property='children'),
    Input(component_id='b_spin_clock', component_property='n_clicks'),
)
def spin_clock(n):
    global sm
    triggered = [p['prop_id'].split('.')[0] for p in dash.callback_context.triggered]
    if 'b_spin_clock' in triggered:
        print('cw')
        sm.move_servo('cw')
    return ''

# zero
@app.callback(
    Output(component_id='ret_zero_angle', component_property='children'),
    Input(component_id='b_zero_angle', component_property='n_clicks'),
)
def reset_zero(n):
    global sm
    triggered = [p['prop_id'].split('.')[0] for p in dash.callback_context.triggered]
    if 'b_zero_angle' in triggered:
        print('zero')
        sm.angle = 0
        sm.update_fig()
    return ''

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