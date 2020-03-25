from uncertainties import ufloat

# Std deviations are a combination of resolution, calibration uncertainties, deviation, repatibility, errors and homogeneity

# Temperature
T = ufloat(293.15, 1.74)
# Atmospheric pressure
P = ufloat(101325, 43)
# Air humidity
H = ufloat(0.5, 0.03)
# Differential pressure measured at ref position
Pdyn = ufloat(60, 12)
# Head Pitot coefficient
k = ufloat(1.003, 0.00691)

Rho = (P-0.378*H*10**(10.202435-(1736.2356/(T-39.05))))/(287.057*T)
v = k*(2*Pdyn/Rho)**0.5

print('v = ', v)
