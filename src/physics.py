def air_density(altitude) -> float: #kg/m3
    return 1 

def drag_force(drag_coeff, velocity, area, fluid_density):
    return 0.5 * drag_coeff * area * fluid_density * velocity**2