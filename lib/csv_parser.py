import csv


class CSVParserNoOutputModelException(Exception):
    def __init__(self):
        self.message = "CSV Parser should have a output model associated!"


class CSVParserOutputModelUnmatchException(Exception):
    def __init__(self, row, index):
        self.message = f"Ooops! Looks like your output model doesn't match CSV format for row at index {index}: {row}"


class CSVParser:
    def __init__(self, output_model=None, separator=",", skip_column_name=True):
        self.output_model = output_model
        self.separator = separator
        self.skip_column_name = skip_column_name

        if (output_model is None):
            raise CSVParserNoOutputModelException()

    def __repr__(self):
        return f"{self.__class__}, {self.__dict__}"

    def parse(self, csv_content):
        parsing_result = []
        for index, row in enumerate(csv.reader(csv_content, delimiter=self.separator, )):
            # don't parse column name if option is set
            if index == 0 and self.skip_column_name:
                continue

            try:
                parsing_result.append(self.output_model(*row[:-2]))
            except TypeError:
                raise CSVParserOutputModelUnmatchException(
                    row, index) from None

        return parsing_result
