import math as m
import numpy as np
import matplotlib.pyplot as plt

# All units in SI unless otherwise stated
# Simulation parameters
SIM_DURATION = 100 #s
SIM_TIMESTEP = 0.01 #s

# Physical parameters
GRAVITY = 9.81 #m/s2
def air_density(altitude) -> float: #kg/m3
    return 1 

# Rocket parameters
ROCKET_DRY_MASS = 1 #kg
ROCKET_WET_MASS = 1.3 #kg
ROCET_INITIAL_MMOI = 0.045 #kg m2
ROCKET_MAX_THRUST = 1.5 * ROCKET_WET_MASS * GRAVITY # N
ROCKET_BURN_TIME = 15 #s
ROCKET_MAX_GIMBAL_ANGLE = m.radians(5.0) #rad
ROCKET_HEIGHT = 1 #m
ROCKET_DIAMETER = 0.15 #m
ROCKET_INITIAL_POSITION = [0.0, 0.0, 0.0] # x [m], z [m], theta [rad]
ROCKET_INITIAL_VELOCITY = [0.0, 0.0, 0.0] # x' [m/s], z' [m/s], theta' [rad/s]
ROCKET_INITIAL_GIMBAL_ANGLE = m.radians(.01) #rad

def rocket_drag_coeff(angle_of_attack=0) -> float: 
    return 0.5

def rocket_fuel_consumption(thrust) -> float: #kg/s
    if thrust <= 0:
        return 0
    fuel_total_mass = ROCKET_WET_MASS -  ROCKET_DRY_MASS
    return fuel_total_mass / ROCKET_BURN_TIME

def rocket_centre_gravity(mass) -> float: #m
    return 0.5 * ROCKET_HEIGHT * (2 - mass / ROCKET_WET_MASS )

def rocket_centre_pressure() -> float: #m
    # Assume constant
    return 0.5 * ROCKET_HEIGHT 

def rocket_mmoi(mass) -> float: #kg m2
    initial_mmoi = 0.045
    return mass / ROCKET_WET_MASS * initial_mmoi

def rocket_vel_u(vx, vz, theta):
    if theta in [m.radians(0), m.radians(180)]:
        return vz
    return vx/m.sin(theta)

time = 0.0

# graph data
times_history = np.zeros(m.ceil(SIM_DURATION / SIM_TIMESTEP + 1))
positions_history = np.zeros((m.ceil(SIM_DURATION / SIM_TIMESTEP + 1), 3))
i = 0

position = ROCKET_INITIAL_POSITION.copy()
velocity = ROCKET_INITIAL_VELOCITY.copy()
acc = [0.0, 0.0, 0.0]
area = 0.25 * m.pi * ROCKET_DIAMETER ** 2
mass = ROCKET_WET_MASS
phi = ROCKET_INITIAL_GIMBAL_ANGLE
while time < SIM_DURATION:

    thrust = ROCKET_MAX_THRUST if time < ROCKET_BURN_TIME else 0.0
    vel_u = rocket_vel_u(velocity[0], velocity[1], position[2])
    drag = 0.5 * rocket_drag_coeff() * air_density(position[1]) * area * vel_u**2
    lift = 0.0 # ignoring lift contribution for now

    acc[0] = 1 / mass * (thrust * m.sin(position[2] + phi) - drag*m.sin(position[2]) - lift*m.cos(position[2]))
    acc[1] = 1 / mass * (thrust*m.cos(position[2]+phi) - drag*m.cos(position[2]) + lift*m.sin(position[2])) - GRAVITY
    acc[2] = 1 / rocket_mmoi(mass) * (- thrust * m.sin(phi) * rocket_centre_gravity(mass) + lift * (rocket_centre_gravity(mass) - rocket_centre_pressure()))

    velocity[0] += acc[0] * SIM_TIMESTEP
    velocity[1] += acc[1] * SIM_TIMESTEP
    velocity[2] += acc[2] * SIM_TIMESTEP
    
    position[0] += velocity[0] * SIM_TIMESTEP
    position[1] += velocity[1] * SIM_TIMESTEP
    position[2] += velocity[2] * SIM_TIMESTEP

    mass -= rocket_fuel_consumption(thrust) * SIM_TIMESTEP

    if position[1] < 0:
        print(f'Rocket landed/crashed. Time: {time:.2f}')
        break

    times_history[i] = time
    positions_history[i][0] = position[0]
    positions_history[i][1] = position[1]
    positions_history[i][2] = position[2]
    i += 1 
    time += SIM_TIMESTEP

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fig.subplots_adjust(hspace=1.5)

ax1.plot(times_history[:i-1], positions_history[:i-1,0])
ax1.set_xlabel('time [s]')
ax1.set_ylabel('x [m]')
ax1.set_title('X over time')
ax1.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax1.get_xaxis_transform(), color='red')
ax1.grid(True)

ax2.plot(times_history[:i-1], positions_history[:i-1,1])
ax2.set_xlabel('time [s]')
ax2.set_ylabel('z [m]')
ax2.set_title('Z over time')
ax2.vlines([ROCKET_BURN_TIME], 0, 1, transform=ax2.get_xaxis_transform(), color='red')
ax2.grid(True)

ax3.plot(positions_history[:i-1,0], positions_history[:i-1,1])
ax3.set_xlabel('x [m]')
ax3.set_ylabel('z [m]')
ax3.set_title('Trajectory')
ax3.grid(True)

plt.show()