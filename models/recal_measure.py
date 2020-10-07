import numpy as np

from collections import namedtuple
from lib.compute import (compute_rho_with_uncertaintes,
                         compute_u_with_uncertainties, compute_average_and_stdev)
from uncertainties import (ufloat, unumpy)


RecalMeasures = namedtuple('RecalMeasures', [
                           't', 'deltaP_z', 'deltaP_rap', 'deltaP_ref', 'temp', 'hr', 'p_atmo', ])

RecalProperties = namedtuple(
    'RecalProperties', ['filename', 'u_ref', 'alpha_u_ref', 'alpha_u_ref_std', 'alpha_u_rap', 'aalpha_u_rap_std'])


def compute_recal_measures(name, recal_measures, k_z):

    # Transform raw measurements in deltaP ref, deltaP z and rho ufloats (with uncertainties)

    measures_with_uncertainties = [
        (
            t,
            ufloat(deltaP_ref, 0, 'deltaP_ref'),
            ufloat(deltaP_rap, 0, 'deltaP_rap'),
            ufloat(deltaP_z, 4, 'deltaP_z'),
            compute_rho_with_uncertaintes(
                temperature, hr, p_atmo, 1.74, 0.86, 86)
        )
        for (t, deltaP_z, deltaP_rap, deltaP_ref, temperature, hr, p_atmo) in recal_measures
    ]

    # Transform ufloats deltaP measurements into speed measurements (with uncertainties)

    u_measures = [
        (t, compute_u_with_uncertainties(ufloat(deltaP_ref.n, deltaP_ref.s), ufloat(rho.n, rho.s), ufloat(1, 0)),
         compute_u_with_uncertainties(
             ufloat(deltaP_rap.n, deltaP_rap.s), ufloat(rho.n, rho.s), ufloat(1, 0)),
         compute_u_with_uncertainties(
            ufloat(deltaP_z.n, deltaP_z.s), ufloat(rho.n, rho.s), ufloat(k_z, 0.01))
         )
        for (t, deltaP_ref, deltaP_rap, deltaP_z, rho) in measures_with_uncertainties
    ]

    u_ref_average = np.mean(unumpy.nominal_values(
        [u_ref for (_, u_ref, _, _) in u_measures]))

    u_rap_average = np.mean(unumpy.nominal_values(
        [u_rap for (_, _, u_rap, _) in u_measures]))

    # Compute the alpha coefficient in speed, for each measure

    alpha_u_ref = [u_z / u_ref for (_, u_ref, _, u_z) in u_measures]
    alpha_u_rap = [u_z / u_rap for (_, _, u_rap, u_z) in u_measures]

    # Compute alpha average avec std, combination of alpha std of each measure average and std deviation of the alpha coefficient

    alpha_u_ref_average = np.mean(unumpy.nominal_values(alpha_u_ref))
    alpha_u_ref_std = (np.std(unumpy.nominal_values(alpha_u_ref))**2 +
                       np.mean(unumpy.std_devs(alpha_u_ref))**2)**0.5

    alpha_u_rap_average = np.mean(unumpy.nominal_values(alpha_u_rap))
    alpha_u_rap_std = (np.std(unumpy.nominal_values(alpha_u_rap))**2 +
                       np.mean(unumpy.std_devs(alpha_u_rap))**2)**0.5

    return [RecalProperties(name, u_ref_average, alpha_u_ref_average, alpha_u_ref_std, alpha_u_rap_average, alpha_u_rap_std)]


def convert_raw_str_value_to_float(value):
    return float(value)


class RecalMeasureModel:
    def __init__(self,  k_z, name):
        # interface model
        self.parsing_output_model = lambda t, deltaP_z, deltaP_rap, deltaP_ref, temp, hr, p_atmo: RecalMeasures(convert_raw_str_value_to_float(t), convert_raw_str_value_to_float(deltaP_z), convert_raw_str_value_to_float(
            deltaP_rap), convert_raw_str_value_to_float(deltaP_ref), convert_raw_str_value_to_float(temp), convert_raw_str_value_to_float(hr), convert_raw_str_value_to_float(p_atmo))

        self.compute = lambda measures_to_compute: compute_recal_measures(name,
                                                                          measures_to_compute, k_z)

        # specific RecalMeasureModel fields

        self.k_z = k_z
        self.name = name
