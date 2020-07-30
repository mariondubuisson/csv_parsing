import csv
from models.recal_measure import RecalMeasureModel
from tkinter import filedialog
from lib.csv_parser import CSVParser
from os import path
from functools import reduce
# from lib.Param_gradient import param_from_matlab_file

#########################################################################
##                          PROGRAM PARAMETERS                         ##
#########################################################################

# Correction coeff. of the reference delta P measure
A_REF = 1

# correction coeff. of the gradient delta P measure
A_Z = 1

# Head coeff. of the Pitot reference
K_REF = 1

# Head coeff. of the gradient Pitot
K_Z = 1


# Files parameters
prefix = 'XXX'
extension = '.dat'

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

    # Compute
    model_computed_measures = model.compute(parsed_model_measures)

    return model_computed_measures


def get_filename(filename):
    return str(path.basename(filename).replace(prefix, '').replace(extension, ''))


def main(args=None):
    # Open a file selection dialog, restrict to CSV extensions
    csv_file_streams = filedialog.askopenfiles(
        filetypes=[('CSV files', '.csv'), ('Data files', '.dat'), ('All files', '*')])

    pipeline_real_outputs = flatten([
        transformation_pipeline(
            csv_file_stream,
            RecalMeasureModel(
                k_z=K_Z,
                name=get_filename(csv_file_stream.name)
            )
        )
        for csv_file_stream in csv_file_streams])

    # Exploit result, create csv result file
    output_file = filedialog.asksaveasfilename(
        filetypes=[('CSV files', '.csv'), ('All files', '*')],
        defaultextension='.csv')
    with open(output_file, "w", newline="") as result_file:
        result_writer = csv.writer(result_file)
        result_writer.writerow(['Compute parameters'])
        result_writer.writerow(
            ['Correction coeff. of the reference delta P measure', 'a_REF', A_REF])
        result_writer.writerow(
            ['correction coeff. of the gradient delta P measure', 'a_Z', A_Z])
        result_writer.writerow(
            ['Head coeff. of the Pitot reference', 'k_ref', K_REF])
        result_writer.writerow(
            ['Head coeff. of the gradient Pitot', 'k_Z', K_Z])

        result_writer.writerow(list(pipeline_real_outputs[0]._fields))
        for row in pipeline_real_outputs:
            result_writer.writerow(list(row))


if __name__ == "__main__":
    main()
