import csv
from models.pitot_measure import PitotMeasureModel
from tkinter import filedialog
from lib.csv_parser import CSVParser
from os import path
from functools import reduce


def flatten(listOfLists):
    return reduce(list.__add__, listOfLists)


def transformationPipeline(csv_file_stream, model):
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
    return int(path.basename(filename).replace('U10h', '').replace('.csv', ''))


def main(args=None):
    # Open a file selection dialog, restrict to CSV extensions
    csv_file_streams = filedialog.askopenfiles(
        filetypes=(("csv {csv}", "toto files")))

    pipeline_outputs = flatten([
        transformationPipeline(csv_file_stream, PitotMeasureModel(
            get_altitude_from_filename(csv_file_stream.name)))
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
