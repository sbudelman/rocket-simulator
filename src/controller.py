import math as m

from config import SIM_TIMESTEP

class Controller:
    def __init__(self):
        self._setpoint = 0.0
        self._error = 0.0
        self._integral_error = 0.0

    def get_output(self, current_measurement):
        new_error = self.setpoint - current_measurement
        proportional_term =self.kp * new_error
        
        derivative_error = (self._error - new_error) / SIM_TIMESTEP
        integral_term = self.ki * self._integral_error
        
        derivative_term = self.kd * derivative_error
        self._integral_error += new_error
        
        self._error = new_error

        return proportional_term + integral_term + derivative_term

    def set_gains(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    @property
    def setpoint(self):
        return self._setpoint

    @setpoint.setter
    def setpoint(self, target):
        self._setpoint = target