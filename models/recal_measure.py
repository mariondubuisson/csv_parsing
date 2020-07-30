from collections import namedtuple
from lib.compute import (compute_u_from_delta_p,
                         compute_rho, compute_average_and_stdev)

RecalMeasures = namedtuple('RecalMeasures', [
                           't', 'deltaP_z', 'deltaP_rap', 'deltaP_ref', 'temp', 'hr', 'p_atmo', ])

RecalProperties = namedtuple('RecalProperties', ['u_ref', 'alpha_u'])


def compute_recal_measures(recal_measures, k_z):
    rho = [compute_rho(temperature, hr, p_atmo)
           for (temperature, hr, p_atmo) in recal_measures]

    u_measure = [
        (t,
         compute_u_from_delta_p(deltaP_ref, rho, 1),
         compute_u_from_delta_p(deltaP_z, rho, k_z)
         )
        for (t, deltaP_ref, deltaP_z) in recal_measures
    ]

    (u_ref_average, u_ref_std) = compute_average_and_stdev(
        [float(u_ref) for (_, u_ref, _) in u_measure])

    (u_z_average, u_z_std) = compute_average_and_stdev(
        [float(u_z) for (_, _, u_z) in u_measure])

    alpha_u = u_z_average / u_ref_average

    return [RecalProperties(u_ref_average, alpha_u)]


def convert_raw_str_value_to_float(value):
    return float(value)


class RecalMeasureModel:
    def __init__(self, k_z, name):
        # interface model
        self.parsing_outpout_model = lambda t, deltaP_z, deltaP_rap, deltaP_ref, temp, hr, p_atmo: RecalMeasures(convert_raw_str_value_to_float(t), convert_raw_str_value_to_float(deltaP_z), convert_raw_str_value_to_float(
            deltaP_rap), convert_raw_str_value_to_float(deltaP_ref), convert_raw_str_value_to_float(temp), convert_raw_str_value_to_float(hr), convert_raw_str_value_to_float(p_atmo))

        self.compute = lambda measures_to_compute: compute_recal_measures(
            measures_to_compute, k_z)

        # specific RecalMeasureModel fields

        self.k_z = k_z
        self.name = name
