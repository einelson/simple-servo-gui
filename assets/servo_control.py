
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

import plotly.graph_objects as go
from time import sleep

class servo_manager:
    def __init__(self):
        print('init servo manager')
        factory = PiGPIOFactory('127.0.0.1')
        self.servo = AngularServo(18, min_angle=-180, max_angle=180, min_pulse_width=0.0006, max_pulse_width=0.0024, pin_factory=factory)
        self.angle = 0
        # self.init_servo()
        self.update_fig()

    # def __del__(self):
    #     self.pwm.ChangeDutyCycle(0) # this prevents jitter
    #     self.pwm.stop() # stops the pwm on 13
    #     GPIO.cleanup()


    # def init_servo(self):
        
    #     GPIO.setmode(GPIO.BCM)
    #     GPIO.setup(18,GPIO.OUT)

    #     # setup PWM process
    #     self.pwm = GPIO.PWM(self.servo_pin,50) # 50 Hz (20 ms PWM period)
    #     self.pwm.start(0)


    def update_fig(self):
        self.fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = self.angle * -1,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Servo angle", 'font': {'size': 24}},
            # delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
            gauge = {
                'axis': {'range': [-180,180], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                # 'borderwidth': 2,
                # 'bordercolor': "gray",
                # 'steps': [
                #     {'range': [0, 250], 'color': 'cyan'},
                #     {'range': [250, 400], 'color': 'royalblue'}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 490}}))

        self.fig.update_layout(paper_bgcolor = 'rgb(37, 37, 37)', font = {'color': "white", 'family': "Arial"})
        
    def get_fig(self):
        return self.fig


    def move_servo(self, direction):
        # check if angle is going to be too high or low 0 to 180
        if direction == 'cw' and self.angle != 180:
            self.angle += 20
        elif direction == 'ccw' and self.angle != -180:
            self.angle -= 20
        else:
            print('angle too extreme!')
            return

        self.servo.angle = self.angle
        print(self.servo.pulse_width)

        self.update_fig()

    # goto zero
    def goto_zero(self):
        self.angle = 0
        self.servo.angle = (self.angle * 2)
        self.update_fig()


