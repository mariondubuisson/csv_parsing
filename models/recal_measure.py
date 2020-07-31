from collections import namedtuple
from lib.compute import (compute_rho_with_uncertaintes,
                         compute_u_with_uncertainties, compute_average_and_stdev)
from uncertainties import ufloat

RecalMeasures = namedtuple('RecalMeasures', [
                           't', 'deltaP_z', 'deltaP_rap', 'deltaP_ref', 'temp', 'hr', 'p_atmo', ])

RecalProperties = namedtuple(
    'RecalProperties', ['filename', 'u_ref', 'alpha_u'])


def compute_recal_measures(name, recal_measures, k_z):

    measure_with_uncertainties = [
        (
            t,
            ufloat(deltaP_ref, 0),
            ufloat(deltaP_z, 4),
            compute_rho_with_uncertaintes(
                temperature, hr, p_atmo, 1.74, 0.86, 86)
        )
        for (t, deltaP_z, _, deltaP_ref, temperature, hr, p_atmo) in recal_measures
    ]

    u_measure = [
        (t, compute_u_with_uncertainties(ufloat(deltaP_ref.n, deltaP_ref.s), ufloat(rho.n, rho.s), ufloat(1, 0)),
         compute_u_with_uncertainties(
            ufloat(deltaP_z.n, deltaP_z.s), ufloat(rho.n, rho.s), ufloat(k_z, 0.01))
         )
        for (t, deltaP_ref, deltaP_z, rho) in measure_with_uncertainties
    ]

    print(u_measure)

    (u_ref_average, u_ref_std) = compute_average_and_stdev(
        [float(u_ref) for (_, u_ref, _) in u_measure])

    (u_z_average, u_z_std) = compute_average_and_stdev(
        [float(u_z) for (_, _, u_z) in u_measure])

    alpha_u_average = u_z_average / u_ref_average

    return [RecalProperties(name, u_ref_average, alpha_u_average)]


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
