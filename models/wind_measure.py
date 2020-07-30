from collections import namedtuple
from lib.compute import (compute_u_from_delta_p, compute_average_and_stdev,
                         compute_delta_p_from_u)

WindMeasures = namedtuple('wind_measures', [
    't', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz', 'p_ref', 'u_gil', 'p_rap'])
WindProperties = namedtuple('WindProperties', [
    'delta_p_ref',
    'u_ref',
    'delta_p_gil',
    'u_gil',
    'alpha_u_ref_gil',
    'alpha_p_ref_gil',
])


def sanitize_wind_measures(wind_measures):
    return [
        (t, p_ref, u_gil)
        for (t, Fx, Fy, Fz, Mx, My, Mz, p_ref, u_gil, p_rap) in wind_measures
        if p_ref > 0 and u_gil > 0
    ]


def compute_wind_measures(wind_measures, rho, k_ref):
    u_measures = [
        (
            t,
            p_ref,
            compute_u_from_delta_p(p_ref, rho, k_ref),
            compute_delta_p_from_u(u_gil, rho),
            u_gil,
        )
        for (t, p_ref, u_gil) in wind_measures
    ]

    alpha_measures = [
        (
            t,
            u_ref/u_gil,
            p_ref/p_gil,

        )
        for (t, p_ref, u_ref, p_gil, u_gil) in u_measures
    ]

    (p_ref_average, _) = compute_average_and_stdev(
        [float(p_ref) for (_, p_ref, _) in wind_measures])
    (u_ref_average, _) = compute_average_and_stdev(
        [float(u_ref) for (_, _, u_ref, _, _) in u_measures])
    (p_gil_average, _) = compute_average_and_stdev(
        [float(p_gil) for (_, _, _, p_gil, _) in u_measures])
    (u_gil_average, _) = compute_average_and_stdev(
        [float(u_gil) for (_, _, u_gil) in wind_measures])
    (alpha_u_ref_gil_average, _) = compute_average_and_stdev(
        [float(alpha_u_ref_gil) for (_, alpha_u_ref_gil, _) in alpha_measures])
    (alpha_p_ref_gil_average, _) = compute_average_and_stdev(
        [float(alpha_p_ref_gil) for (_, _, alpha_p_ref_gil) in alpha_measures])

    return [WindProperties(p_ref_average, u_ref_average, p_gil_average, u_gil_average,
                           alpha_u_ref_gil_average, alpha_p_ref_gil_average,)]


def convert_raw_str_value_to_float(str):
    return float(str.replace(',', '.'))


class wind_measure_model:
    def __init__(self, rho, k_ref):
        # interface model
        self.parsing_output_model = lambda t, Fx, Fy, Fz, Mx, My, Mz, p_ref, u_gil, p_rap: WindMeasures(
            t, Fx, Fy, Fz, Mx, My, Mz, convert_raw_str_value_to_float(p_ref), convert_raw_str_value_to_float(u_gil), p_rap)
        self.sanitize = lambda measures_to_sanitize: sanitize_wind_measures(
            measures_to_sanitize)
        self.compute = lambda measures_to_compute: compute_wind_measures(
            measures_to_compute, rho, k_ref)

        # specific wind_measure_model fields
        self.rho = rho
        self.k_ref = k_ref
