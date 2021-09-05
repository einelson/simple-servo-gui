
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

import plotly.graph_objects as go

class servo_manager:
    def __init__(self):
        print('init servo manager')
        factory = PiGPIOFactory('127.0.0.1')
        self.servo = AngularServo(18, min_angle=-180, max_angle=180, min_pulse_width=0.0006, max_pulse_width=0.0024, pin_factory=factory)
        self.angle = 0
        # self.init_servo()
        self.update_fig()


    def update_fig(self):
        self.fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = self.angle,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Servo angle", 'font': {'size': 24}},
            # delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
            gauge = {
                'axis': {'range': [-90,90], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "white"},
                'bgcolor': "white",
                # 'borderwidth': 2,
                # 'bordercolor': "gray",
                # 'steps': [
                #     {'range': [self.drag_angle, self.drag_angle + 1], 'color': 'blue'}],
                #     {'range': [250, 400], 'color': 'royalblue'}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': self.angle}})) # mult by 2 to get the correct angle

        self.fig.update_layout(paper_bgcolor = 'rgb(37, 37, 37)', font = {'color': "white", 'family': "Arial"})
        
    def get_fig(self):
        return self.fig


    def move_servo(self, angle):
        # update angle
        self.angle = angle
        # servo moves according to angle
        # the - can be removed depending which side of the servo you are looking at
        # the 2 is to translate to the correct angle
        self.servo.angle = (self.angle *-2)
        # update graphic
        self.update_fig()

    # goto zero
    def goto_zero(self):
        self.angle = 0
        self.servo.angle = self.angle
        self.update_fig()
