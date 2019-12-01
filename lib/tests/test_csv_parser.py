import unittest
from lib.csv_parser import CSVParser, CSVParserNoOutputModelException, CSVParserOutputModelUnmatchException
from collections import namedtuple

FakeOutputModel = namedtuple("FakeOutputModel", ["field1", "field2"])
fake_csv_content = ['field1,field2', '2.3,34', '2.4,32']


class TestCSVParser(unittest.TestCase):
    def test_csv_parser_init(self):
        csv_parser = CSVParser(output_model=FakeOutputModel)
        assert csv_parser.output_model == FakeOutputModel
        assert csv_parser.separator == ','

    def test_csv_parser_init_with_custom_separator(self):
        csv_parser = CSVParser(output_model=FakeOutputModel, separator=' ')
        assert csv_parser.output_model == FakeOutputModel
        assert csv_parser.separator == ' '

    def test_csv_parser_init_no_output_model_exception(self):
        with self.assertRaises(CSVParserNoOutputModelException) as context:
            CSVParser()

        assert context.exception.message == 'CSV Parser should have a output model associated!'

    def test_csv_parser_parse_with_default(self):
        csv_parser = CSVParser(output_model=FakeOutputModel)
        parsing_result = csv_parser.parse(fake_csv_content)

        assert parsing_result == [FakeOutputModel(
            field1='2.3', field2='34'), FakeOutputModel(field1='2.4', field2='32')]

    def test_csv_parser_parse_without_skip_column_name(self):
        csv_parser = CSVParser(
            output_model=FakeOutputModel, skip_column_name=False)
        parsing_result = csv_parser.parse(fake_csv_content)

        assert parsing_result == [FakeOutputModel(
            field1='field1', field2='field2'), FakeOutputModel(
            field1='2.3', field2='34'), FakeOutputModel(field1='2.4', field2='32')]

    def test_csv_parser_parse_with_custom_separator_unmatching_csv_separator(self):
        csv_parser = CSVParser(
            output_model=FakeOutputModel, separator=' ')

        with self.assertRaises(CSVParserOutputModelUnmatchException) as context:
            csv_parser.parse(fake_csv_content)

        assert context.exception.message == f"Ooops! Looks like your output model doesn't match CSV format for row at index 1: {['2.3,34']}"

    def test_csv_parser_parse_with_a_row_unmatching_output_model(self):
        csv_parser = CSVParser(
            output_model=FakeOutputModel, separator=' ')

        fake_csv_content_with_unwell_formatted_row = [
            'field1 field2', '2.3 34', '2.4 32', '2.5 36 45', '2.6 23']

        with self.assertRaises(CSVParserOutputModelUnmatchException) as context:
            csv_parser.parse(fake_csv_content_with_unwell_formatted_row)

        assert context.exception.message == f"Ooops! Looks like your output model doesn't match CSV format for row at index 3: {['2.5', '36', '45']}"
