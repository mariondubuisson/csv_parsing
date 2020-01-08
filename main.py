import csv
from models.pitot_measure import PitotMeasureModel
from tkinter import filedialog
from lib.csv_parser import CSVParser
from os import path
from functools import reduce

#########################################################################
##                          PROGRAM PARAMETERS                         ##
#########################################################################

# Correction coeff. of the reference delta P measure
A_REF = 1

# correction coeff. of the gradient delta P measure
A_Z = 1

# Head coeff. of the Pitot reference
K_REF = 1

# Head coeff. of the Pitot reference
K_Z = 1

# air mass volumic in kg/m³
RHO = 1.227

#########################################################################
##                       END PROGRAM PARAMETERS                        ##
#########################################################################


def flatten(listOfLists):
    return reduce(list.__add__, listOfLists)


def transformation_pipeline(csv_file_stream, model):
    # Parse CSV content to get an array of data
    model_parser = CSVParser(
        output_model=model.parsing_output_model, separator="\t")

    parsed_model_measures = model_parser.parse(
        csv_file_stream)

    # Sanitize
    sanitized_model_measures = model.sanitize(parsed_model_measures)

    # Compute
    model_computed_measures = model.compute(sanitized_model_measures)

    return model_computed_measures


def get_altitude_from_filename(filename):
    return int(path.basename(filename).replace('u15_h_', '').replace('.csv', ''))


def main(args=None):
    # Open a file selection dialog, restrict to CSV extensions
    csv_file_streams = filedialog.askopenfiles(
        filetypes=(("csv {csv}", "toto files")))

    pipeline_outputs = flatten([
        transformation_pipeline(
            csv_file_stream, 
            PitotMeasureModel(
                z=get_altitude_from_filename(csv_file_stream.name),
                a_ref=A_REF,
                a_z=A_Z,
                rho=RHO,
                k_ref=K_REF,
                k_z=K_Z
            )
        )
        for csv_file_stream in csv_file_streams])

    # print(f"pipeline_outputs : {pipeline_outputs}")

    # Exploit result, create csv result file

    with open("Gradient_properties.csv", "w", newline="") as result_file:
        result_writer = csv.writer(result_file)
        result_writer.writerow(list(pipeline_outputs[0]._fields))
        for row in pipeline_outputs:
            result_writer.writerow(list(row))


if __name__ == "__main__":
    main()
