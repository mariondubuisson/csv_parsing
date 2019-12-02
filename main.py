from tkinter import filedialog
from lib.csv_parser import CSVParser
from lib.compute import compute_u_from_delta_p
from models.pitot_measure import PitotMeasure
import math
import statistics
import csv


def main(args=None):
    # Open a file selection dialog, restrict to CSV extensions
    csv_file_stream = filedialog.askopenfile(
        filetypes=(("CSV files ", "csv {csv}")))

    # Parse CSV content to get an array of data
    pitot_measure_parser = CSVParser(output_model=PitotMeasure, separator='\t')
    parsed_pitot_measures = pitot_measure_parser.parse(csv_file_stream)

    # Sanitization
    sanitized_pitot_measures = [(float(t), float(delta_p_ref), float(delta_p_z)) 
                                for (t, delta_p_ref, delta_p_z) in parsed_pitot_measures
                                if float(delta_p_ref) > float(0)
                                    and float(delta_p_z) > float (0)]
    
    # Compute u
    u_measures = [(float(t), compute_u_from_delta_p(delta_p_ref), compute_u_from_delta_p(delta_p_z))
                  for (t, delta_p_ref, delta_p_z) in sanitized_pitot_measures]

    # Averaged u_ref and u_z
    u_ref = [(float(u_ref))
            for (t, u_ref, u_z) in u_measures]
    u_z = [(float(u_z))
            for (t,u_ref, u_z) in u_measures]
    average_u = [statistics.mean(u_ref), statistics.mean(u_z)]
    stdev_u = [statistics.stdev(u_ref), statistics.stdev(u_z)]
    average_title = ["average_u_ref", "average_u_z"]
    stdev_title = ["stdev_u_ref", "stdev_u_z"]
    print(f"{average_title} \n {average_u}")
    print(f"{stdev_title} \n {stdev_u}")

    # Exploit result, create csv result file
    with open('results_u.csv', 'w', newline='') as result_file:
        result_writer = csv.writer(result_file, delimiter=' ')
        for u_measure in u_measures:
            result_writer.writerow(list(u_measure))

    


if __name__ == "__main__":
    main()
