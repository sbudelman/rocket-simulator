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

# graph data
n_plots = 11
n_simulation_steps = m.ceil(SIM_DURATION / SIM_TIMESTEP + 1)
graph = GraphHandler(size=[n_plots, n_simulation_steps])
while time < SIM_DURATION:

    rocket.update(time)

    if rocket.position[1] < 0:
        print(f'Rocket landed/crashed. Time: {time:.2f}')
        break

    graph.collect([time, *rocket.position, *rocket.velocity, *rocket.acc, rocket.thrust])
    time += SIM_TIMESTEP

ax1 = graph.define_plot(0, 1, xlabel='time [s]', ylabel='x [m]', title='X over time')
ax1.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax1.get_xaxis_transform(), color='red')

ax2 = graph.define_plot(0, 2, xlabel='time [s]', ylabel='z [m]', title='Z over time')
ax2.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax2.get_xaxis_transform(), color='red')

ax3 = graph.define_plot(0, 3, xlabel='time [s]', ylabel='theta [rad]', title='Theta over time')
ax3.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax3.get_xaxis_transform(), color='red')

ax4 = graph.define_plot(0, 4, xlabel='time [s]', ylabel='vel X [m/s]', title='Vel X over time')
ax4.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax4.get_xaxis_transform(), color='red')

ax5 = graph.define_plot(0, 5, xlabel='time [s]', ylabel='vel Z [m/s]', title='Vel Z over time')
ax5.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax5.get_xaxis_transform(), color='red')

ax6 = graph.define_plot(0, 6, xlabel='time [s]', ylabel='vel theta [rad/s]', title='Vel Theta over time')
ax6.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax6.get_xaxis_transform(), color='red')

ax7 = graph.define_plot(0, 7, xlabel='time [s]', ylabel='acc X [m/s2]', title='Acc X over time')
ax7.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax7.get_xaxis_transform(), color='red')

ax8 = graph.define_plot(0, 8, xlabel='time [s]', ylabel='acc Z [m/s2]', title='Acc Z over time')
ax5.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax8.get_xaxis_transform(), color='red')

ax9 = graph.define_plot(0, 9, xlabel='time [s]', ylabel='acc theta [rad/s2]', title='Acc Theta over time')
ax9.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax9.get_xaxis_transform(), color='red')

ax10 = graph.define_plot(1, 2, xlabel='x [m]', ylabel='z [m]', title='Trajectory')

ax11 = graph.define_plot(0, 10, xlabel='time [s]', ylabel='thrust [N]', title='Thrust over time')

graph.show()