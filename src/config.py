import math as m

# All units in SI unless otherwise stated
# Simulation parameters
SIM_DURATION = 100 #s
SIM_TIMESTEP = 0.01 #s

# Physical parameters
GRAVITY = 9.81 #m/s2


# Rocket parameters
ROCKET_DRY_MASS = 1 #kg
ROCKET_WET_MASS = 1.3 #kg
ROCKET_INITIAL_MMOI = 0.045 #kg m2
ROCKET_MAX_THRUST = 2.5 * ROCKET_WET_MASS * GRAVITY # N
ROCKET_BURN_TIME = 20 #s
ROCKET_MAX_GIMBAL_ANGLE = m.radians(5.0) #rad
ROCKET_HEIGHT = 1 #m
ROCKET_DIAMETER = 0.15 #m
ROCKET_INITIAL_POSITION = [0.0, 0.0, m.radians(0.1)] # x [m], z [m], theta [rad]
ROCKET_INITIAL_VELOCITY = [0.0, 0.0, 0.0] # x' [m/s], z' [m/s], theta' [rad/s]
ROCKET_INITIAL_GIMBAL_ANGLE = m.radians(.0) #rad