import math
import statistics


def compute_average_and_stdev(list):
    return (statistics.mean(list), statistics.stdev(list))


def compute_u_from_delta_p(delta_p, rho, k):
    return k*math.sqrt(float(delta_p)*2/float(rho))


def turbulence_intensity_from_u(u, stdev_u):
    return float(stdev_u)/float(u)


def compute_delta_p_from_u(u, rho):
    return rho*u*u/2
