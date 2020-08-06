import math
import statistics
from uncertainties import (ufloat, umath)


def compute_average_and_stdev(list):
    return (statistics.mean(list), statistics.stdev(list))


def compute_u_from_delta_p(delta_p, rho, k):
    return k*math.sqrt(float(delta_p)*2/float(rho))

# Use compute_u_with_uncertainties if you use ufloat variable (umath package)


def compute_u_with_uncertainties(delta_p, rho, k):
    return k * umath.sqrt(delta_p * 2 / rho)


def turbulence_intensity_from_u(u, stdev_u):
    return float(stdev_u)/float(u)


def compute_delta_p_from_u(u, rho):
    return rho*u*u/2


def compute_rho(t, hr, p_atmo):
    return (p_atmo*100-0.378*hr/100*10**(10.202435-(1736.2356/(t+273.15-39.05))))/(287.057*(t+273.15))


def compute_rho_with_uncertaintes(t, hr, p, u_t, u_hr, u_p):
    return ((ufloat(p, u_p, 'p_atmo')*100-0.378*ufloat(hr, u_hr, 'hr')/100*10**(10.202435-(1736.2356/(ufloat(t, u_t, 't')+273.15-39.05))))/(287.057*(ufloat(t, u_t, 't')+273.15)))
