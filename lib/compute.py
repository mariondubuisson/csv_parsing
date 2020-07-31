import math
import statistics
from uncertainties import (ufloat, umath)


def compute_average_and_stdev(list):
    return (statistics.mean(list), statistics.stdev(list))


def compute_u_from_delta_p(delta_p, rho, k):
    return k*math.sqrt(float(delta_p)*2/float(rho))


def compute_u_with_uncertainties(delta_p, rho, k):
    return ufloat(k.n, k.s) * umath.sqrt(ufloat(delta_p.n, delta_p.s) * 2 / ufloat(rho.n, rho.s))


def turbulence_intensity_from_u(u, stdev_u):
    return float(stdev_u)/float(u)


def compute_delta_p_from_u(u, rho):
    return rho*u*u/2


def compute_rho(t, hr, p_atmo):
    return (p_atmo*100-0.378*hr/100*10**(10.202435-(1736.2356/(t+273.15-39.05))))/(287.057*(t+273.15))


def compute_rho_with_uncertaintes(t, hr, p, u_t, u_hr, u_p):
    return ((ufloat(p, u_p)*100-0.378*ufloat(hr, u_hr)/100*10**(10.202435-(1736.2356/(ufloat(t, u_t)+273.15-39.05))))/(287.057*(ufloat(t, u_t)+273.15)))
