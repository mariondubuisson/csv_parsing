import math


def compute_u_from_delta_p(delta_p):
    return math.sqrt(float(delta_p)*2/1.225)

def turbulence_intensity_from_u(u, stdev_u):
    return float(stdev_u)/float(u)
