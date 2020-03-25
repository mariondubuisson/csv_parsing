from collections import namedtuple
from lib.compute import (compute_u_from_delta_p, compute_average_and_stdev,
                         turbulence_intensity_from_u)

# Be sure your PitotMeasure model is correct, or adapt it, but don't forget to also modify
# sanitize_pitot_measures with the good number of elements
# self.parsing_output_model with the good number of elements

PitotMeasure = namedtuple(
    'PitotMeasure', ['t', 'delta_p_ref', 'delta_p_z'])

WindProperties = namedtuple('WindProperties', [
    'z',
    'delta_p_ref',
    'delta_p_z',
    'u_ref_average',
    'u_ref_stdev',
    'u_z_average',
    'u_z_stdev',
    'turbulence_intensity',
    'Pdyn'
])


def sanitize_pitot_measures(pitot_measures, a_ref, a_z):
    return [
        (float(t), a_ref*float(delta_p_ref), a_z*float(delta_p_z))
        for (t, delta_p_ref, delta_p_z) in pitot_measures
        if float(delta_p_ref) > 0 and float(delta_p_z) > 0
    ]


def compute_pitot_measures(pitot_measures, rho, k_ref, k_z, z):
    u_measures = [
        (
            float(t),
            compute_u_from_delta_p(delta_p_ref, rho)*k_ref,
            compute_u_from_delta_p(delta_p_z, rho)*k_z,
        )
        for (t, delta_p_ref, delta_p_z) in pitot_measures]

    (P_ref_average, _) = compute_average_and_stdev(
        [float(delta_p_ref) for (_, delta_p_ref, _) in pitot_measures])
    (P_z_average, _) = compute_average_and_stdev(
        [float(delta_p_z) for (_, _, delta_p_z) in pitot_measures])
    (u_ref_average, u_ref_stdev) = compute_average_and_stdev(
        [float(u_ref) for (_, u_ref, _) in u_measures])
    (u_z_average, u_z_stdev) = compute_average_and_stdev(
        [float(u_z) for (_, _, u_z) in u_measures])
    turbulence_intensity = turbulence_intensity_from_u(u_z_average, u_z_stdev)
    Pdyn = P_z_average/P_ref_average

    return [WindProperties(z, P_ref_average, P_z_average, u_ref_average, u_ref_stdev, u_z_average,
                           u_z_stdev, turbulence_intensity, Pdyn)]


def convert_raw_str_value_to_float(str):
    return float(str.replace(',', '.'))


class PitotMeasureModel:
    def __init__(self, a_ref, a_z, rho, k_ref, k_z, z):
        # interface model
        self.parsing_output_model = lambda t, delta_p_ref, delta_p_z: PitotMeasure(
            t, convert_raw_str_value_to_float(delta_p_ref), convert_raw_str_value_to_float(delta_p_z))
        self.sanitize = lambda measures_to_sanitize: sanitize_pitot_measures(
            measures_to_sanitize, a_ref, a_z)
        self.compute = lambda measures_to_compute: compute_pitot_measures(
            measures_to_compute, rho, k_ref, k_z, z)

        # specific PitotMeasureModel fields
        self.a_ref = a_ref
        self.a_z = a_z
        self.rho = rho
        self.k_ref = k_ref
        self.k_z = k_z
        self.z = z
