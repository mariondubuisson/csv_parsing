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


def compute_rho(t, hr, p_atmo):
    return (p_atmo*100-0.378*hr/100*10**(10.202435-(1736.2356/(t+273.15-39.05))))/(287.057*(t+273.15))
