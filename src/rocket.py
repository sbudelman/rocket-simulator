import math as m
from controller import Controller
import physics
from config import *

class Rocket:
    def __init__(self, **kwargs):
        self.mass_wet = kwargs.get('mass_wet')
        self.mass_dry = kwargs.get('mass_dry')
        self.mass = self.mass_wet
        self.initial_mmoi = kwargs.get('initial_mmoi')
        self.max_thrust = kwargs.get('max_thrust')
        self.burn_time = kwargs.get('burn_time')
        self.max_gimbal_angle = kwargs.get('max_gimbal_angle')
        self.height = kwargs.get('max_gimbal_angle')
        self.diameter = kwargs.get('max_gimbal_angle')
        self.position = kwargs.get('initial_position')
        self.velocity = kwargs.get('initial_velocity')
        self.gimbal_angle = kwargs.get('initial_gimbal_angle')

        self.thrust = 0.0
        self.drag = 0.0
        self.lift = 0.0

        self.acc = [0.0, 0.0, 0.0]
        self.area = 0.25 * m.pi * self.diameter ** 2

        self._controller = None

    def update(self, time):
        self.update_phi()
        self.update_thrust(time)
        self.update_drag()
        self.update_lift()
        self.update_kinematics()
        self.update_mass()

    def drag_coeff(self) -> float: 
        return 0.5

    def fuel_consumption(self) -> float: #kg/s
        if self.thrust <= 0:
            return 0
        return (self.mass_wet - self.mass_dry) / self.burn_time

    def centre_gravity(self) -> float: #m
        return 0.5 * self.height * (2 - self.mass / self.mass_wet )

    def centre_pressure(self) -> float: #m
        # Assume constant
        return 0.5 * self.height 

    def mmoi(self) -> float: #kg m2
        return self.mass / self.mass_wet * self.initial_mmoi

    def update_thrust(self, time):
        self.thrust = self.max_thrust if time < self.burn_time else 0.0

    def get_velocity_u(self):
        vx = self.velocity[0]
        vz = self.velocity[1]
        theta = self.position[2]
        
        if theta not in [m.radians(0), m.radians(180)]:
            return vx/m.sin(self.position[2])

        return vz

    def update_drag(self):
        rho = physics.air_density(self.position[1])
        u = self.get_velocity_u()
        self.drag = physics.drag_force(self.drag_coeff(), u, self.area, rho)
    
    def update_lift(self):
        self.lift =  0.0 # ignoring lift contribution for now

    def update_kinematics(self):
        self.acc[0] = 1 / self.mass * (self.thrust*m.sin(self.position[2] + self.phi) - self.drag*m.sin(self.position[2]) - self.lift*m.cos(self.position[2]))
        self.acc[1] = 1 / self.mass * (self.thrust*m.cos(self.position[2] + self.phi) - self.drag*m.cos(self.position[2]) + self.lift*m.sin(self.position[2])) - GRAVITY
        self.acc[2] = 1 / self.mmoi() * (- self.thrust * m.sin(self.phi) * self.centre_gravity() + self.lift * (self.centre_gravity() - self.centre_pressure()))

        self.velocity[0] += self.acc[0] * SIM_TIMESTEP
        self.velocity[1] += self.acc[1] * SIM_TIMESTEP
        self.velocity[2] += self.acc[2] * SIM_TIMESTEP
        
        self.position[0] += self.velocity[0] * SIM_TIMESTEP
        self.position[1] += self.velocity[1] * SIM_TIMESTEP
        self.position[2] += self.velocity[2] * SIM_TIMESTEP

    def update_mass(self):
        self.mass -= self.fuel_consumption() * SIM_TIMESTEP

    @property
    def phi(self):
        return self.gimbal_angle

    @phi.setter
    def phi(self, angle):
        self.gimbal_angle = angle

    @property
    def controller(self) -> Controller:
        return self._controller

    @controller.setter
    def controller(self, controller):
        if self._controller is None:
            self._controller = controller
        else:
            ValueError("A controller has already been defined for this rocket. Cannot be replaced.")

    def update_phi(self):
        self.phi = self.controller.get_output(self.position[2])
