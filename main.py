from tkinter import filedialog
from lib.csv_parser import CSVParser
from lib.compute import compute_u_from_delta_p
from models.pitot_measure import PitotMeasure
import math
import csv


def main(args=None):
    # Open a file selection dialog, restrict to CSV extensions
    csv_file_stream = filedialog.askopenfile(
        filetypes=(("CSV files ", "csv {csv}")))

    # Parse CSV content to get an array of data
    pitot_measure_parser = CSVParser(output_model=PitotMeasure, separator='\t')
    parsed_pitot_measures = pitot_measure_parser.parse(csv_file_stream)

    # Sanitization
    

    # Compute u
    u_measures = [(float(t), compute_u_from_delta_p(delta_p_ref), compute_u_from_delta_p(delta_p_z))
                  for (t, delta_p_ref, delta_p_z) in parsed_pitot_measures]

    # Exploit result, create csv result file
    with open('results.csv', 'w', newline='') as result_file:
        result_writer = csv.writer(result_file, delimiter=' ')
        for u_measure in u_measures:
            result_writer.writerow(list(u_measure))


if __name__ == "__main__":
    main()
