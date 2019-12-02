from tkinter import filedialog
from lib.csv_parser import CSVParser
from lib.compute import compute_u_from_delta_p
from lib.compute import turbulence_intensity_from_u
from models.pitot_measure import PitotMeasure
import statistics
import csv


def main(args=None):
    # Open a file selection dialog, restrict to CSV extensions
    csv_file_stream = filedialog.askopenfile(
        filetypes=(("CSV files ", "csv {csv}")))

    # Improvment : Store the altitude

    # Parse CSV content to get an array of data
    pitot_measure_parser = CSVParser(
        output_model=PitotMeasure, separator="\t")

    parsed_pitot_measures = pitot_measure_parser.parse(
        csv_file_stream)

    # Sanitization
    sanitized_pitot_measures = [
        (float(t), float(delta_p_ref), float(delta_p_z))
        for (t, delta_p_ref, delta_p_z) in parsed_pitot_measures
        if float(delta_p_ref) > float(0) and float(delta_p_z) > float(0)
    ]

    # Compute u
    u_measures = [
        (
            float(t),
            compute_u_from_delta_p(delta_p_ref),
            compute_u_from_delta_p(delta_p_z),
        )
        for (t, delta_p_ref, delta_p_z) in sanitized_pitot_measures
    ]

    # Averaged u
    # Improvement : call a method from .lib
    u_ref = [(float(u_ref)) for (t, u_ref, u_z) in u_measures]
    u_z = [(float(u_z)) for (t, u_ref, u_z) in u_measures]
    u_ref = [statistics.mean(u_ref), statistics.stdev(u_ref)]
    u_z = [statistics.mean(u_z), statistics.stdev(u_z)]
    turbulence = (
        float(turbulence_intensity_from_u(average_u_z, stdev_u_z))
        for (average_u_z, stdev_u_z) in u_z
    )

    # Improvment : store the results in a tab for each altitude
    print(f"u_ref {u_ref}")
    print(f"u_z {u_z}")
    print(f"turbulence_intensity {turbulence}")

    # Exploit result, create csv result file
    # Improvement : create a unique csv result file for all altitude with
    # averaged, stdev and turbulence values
    with open("results_u.csv", "w", newline="") as result_file:
        result_writer = csv.writer(result_file, delimiter=" ")
        for u_measure in u_measures:
            result_writer.writerow(list(u_measure))


if __name__ == "__main__":
    main()
