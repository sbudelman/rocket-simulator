import math as m
from config import *
from controller import Controller
from graphs import GraphHandler
from rocket import Rocket

rocket_config = {
    'mass_wet': ROCKET_WET_MASS,
    'mass_dry': ROCKET_DRY_MASS,
    'initial_mmoi': ROCKET_INITIAL_MMOI,
    'max_thrust': ROCKET_MAX_THRUST,
    'burn_time': ROCKET_BURN_TIME,
    'max_gimbal_angle': ROCKET_MAX_GIMBAL_ANGLE,
    'height': ROCKET_HEIGHT,
    'diameter': ROCKET_DIAMETER,
    'initial_position': ROCKET_INITIAL_POSITION,
    'initial_velocity': ROCKET_INITIAL_VELOCITY,
    'initial_gimbal_angle': ROCKET_INITIAL_GIMBAL_ANGLE,
}

rocket = Rocket(**rocket_config)
phi_controller = Controller()
rocket.controller = phi_controller
rocket.controller.setpoint = 0.0
rocket.controller.set_gains(0.0, 0.0, 0.0)

time = 0.0

# graph data0
graph = GraphHandler(5, size=[5, m.ceil(SIM_DURATION / SIM_TIMESTEP + 1)])
while time < SIM_DURATION:

    rocket.update(time)

    if rocket.position[1] < 0:
        print(f'Rocket landed/crashed. Time: {time:.2f}')
        break

    graph.collect([time, *rocket.position, rocket.thrust])
    time += SIM_TIMESTEP

ax1 = graph.define_plot(0, 1, xlabel='time [s]', ylabel='x [m]', title='X over time')
ax1.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax1.get_xaxis_transform(), color='red')

ax2 = graph.define_plot(0, 2, xlabel='time [s]', ylabel='z [m]', title='Z over time')
ax2.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax2.get_xaxis_transform(), color='red')

ax3 = graph.define_plot(0, 3, xlabel='time [s]', ylabel='theta [rad]', title='Theta over time')
ax3.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax3.get_xaxis_transform(), color='red')

ax4 = graph.define_plot(1, 2, xlabel='x [m]', ylabel='z [m]', title='Trajectory')

ax5 = graph.define_plot(0, 4, xlabel='time [s]', ylabel='thrust [N]', title='Thrust over time')

graph.show()