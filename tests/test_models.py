# -*- coding: utf-8 -*-

import unittest

from src.models import FileModel, Aggregate


class FileModelTest(unittest.TestCase):

    def setUp(self):
        self.filemodel = FileModel('www', 0, 0, '-', 0, '-')

    def test_model(self):

        self.assertTrue(hasattr(self.filemodel.__attrs_attrs__, 'url'))
        self.assertTrue(self.filemodel.__attrs_attrs__.url.converter is str)
        self.assertTrue(self.filemodel.__attrs_attrs__.url.type is str)
        self.assertIsNotNone(self.filemodel.__attrs_attrs__.url.validator)

        self.assertTrue(hasattr(self.filemodel.__attrs_attrs__, 'qty_lines'))
        self.assertTrue(
            self.filemodel.__attrs_attrs__.qty_lines.converter is int)
        self.assertTrue(self.filemodel.__attrs_attrs__.qty_lines.type is int)
        self.assertIsNotNone(
            self.filemodel.__attrs_attrs__.qty_lines.validator)

    def test_validate_url_value_ok(self):
        self.filemodel.__attrs_attrs__.url.validator(
            self.filemodel,
            self.filemodel.__attrs_attrs__.url,
            'www.google.com.br')

    def test_validate_url_value_invalid(self):
        self.\
            assertRaises(ValueError,
                         self.filemodel.__attrs_attrs__.url.validator,
                         self.filemodel,
                         self.filemodel.__attrs_attrs__.url,
                         -10)

    def test_validate_url_value_invalid_message(self):
        with self.assertRaises(ValueError) as error:
            self.filemodel.__attrs_attrs__.url.validator(
                self.filemodel,
                self.filemodel.__attrs_attrs__.url,
                -10)
        self.assertEqual(error.exception.__str__(),
                         f"{self.filemodel.__attrs_attrs__.url.name}" \
                         " must be string.")

    def test_validate_qty_lines_value_ok(self):
        self.filemodel.__attrs_attrs__.qty_lines.validator(
            self.filemodel,
            self.filemodel.__attrs_attrs__.qty_lines,
            10)

    def test_validate_qty_lines_value_invalid(self):
        self.\
            assertRaises(ValueError,
                         self.filemodel.__attrs_attrs__.qty_lines.validator,
                         self.filemodel,
                         self.filemodel.__attrs_attrs__.qty_lines,
                         -2)

    def test_validate_qty_lines_value_invalid_message(self):
        with self.assertRaises(ValueError) as error:
            self.filemodel.__attrs_attrs__.qty_lines.validator(
                self.filemodel,
                self.filemodel.__attrs_attrs__.qty_lines,
                -10)
        self.assertEqual(error.exception.__str__(),
                         f"{self.filemodel.__attrs_attrs__.qty_lines.name}" \
                         " must be bigger or equal to 0.")

    def test_validate_size_file_value_ok(self):
        self.filemodel.__attrs_attrs__.size_file.validator(
            self.filemodel,
            self.filemodel.__attrs_attrs__.size_file,
            10)

    def test_validate_size_file_value_invalid(self):
        self.\
            assertRaises(ValueError,
                         self.filemodel.__attrs_attrs__.size_file.validator,
                         self.filemodel,
                         self.filemodel.__attrs_attrs__.size_file,
                         -2)

    def test_validate_size_file_value_invalid_message(self):
        with self.assertRaises(ValueError) as error:
            self.filemodel.__attrs_attrs__.size_file.validator(
                self.filemodel,
                self.filemodel.__attrs_attrs__.size_file,
                -10)
        self.assertEqual(error.exception.__str__(),
                         f"{self.filemodel.__attrs_attrs__.size_file.name}" \
                         " must be bigger or equal to 0.")

    def test_validate_unit_value_ok(self):
        self.filemodel.__attrs_attrs__.unit.validator(
            self.filemodel,
            self.filemodel.__attrs_attrs__.unit,
            "KB")

    def test_validate_unit_value_invalid(self):
        self.\
            assertRaises(ValueError,
                         self.filemodel.__attrs_attrs__.unit.validator,
                         self.filemodel,
                         self.filemodel.__attrs_attrs__.unit,
                         None)

    def test_validate_unit_value_invalid_message_not_string(self):
        with self.assertRaises(ValueError) as error:
            self.filemodel.__attrs_attrs__.unit.validator(
                self.filemodel,
                self.filemodel.__attrs_attrs__.unit,
                None)
        self.assertEqual(error.exception.__str__(),
                         f"{self.filemodel.__attrs_attrs__.unit.name}" \
                         " must be string.")

    def test_validate_unit_value_invalid_message_not_valid(self):
        with self.assertRaises(ValueError) as error:
            self.filemodel.__attrs_attrs__.unit.validator(
                self.filemodel,
                self.filemodel.__attrs_attrs__.unit,
                1)
        self.assertEqual(error.exception.__str__(),
                         f"{self.filemodel.__attrs_attrs__.unit.name}" \
                         " must be Bytes, KB, MB.")

    def test_validate_is_file_value_ok(self):
        self.filemodel.__attrs_attrs__.is_file.validator(
            self.filemodel,
            self.filemodel.__attrs_attrs__.is_file,
            0)

        self.filemodel.__attrs_attrs__.is_file.validator(
            self.filemodel,
            self.filemodel.__attrs_attrs__.is_file,
            1)

    def test_validate_is_file_value_invalid(self):
        self.\
            assertRaises(ValueError,
                         self.filemodel.__attrs_attrs__.is_file.validator,
                         self.filemodel,
                         self.filemodel.__attrs_attrs__.is_file,
                         2)

    def test_validate_is_file_value_invalid_message(self):
        with self.assertRaises(ValueError) as error:
            self.filemodel.__attrs_attrs__.is_file.validator(
                self.filemodel,
                self.filemodel.__attrs_attrs__.is_file,
                -10)
        self.assertEqual(error.exception.__str__(),
                         f"{self.filemodel.__attrs_attrs__.is_file.name}" \
                         " must be 0 or 1.")

    def test_validate_extensions_file_url_value_ok(self):
        self.filemodel.__attrs_attrs__.extensions_file_url.validator(
            self.filemodel,
            self.filemodel.__attrs_attrs__.extensions_file_url,
            'py')

    def test_validate_extensions_file_url_value_invalid(self):
        self.\
            assertRaises(ValueError,
                         self.filemodel.__attrs_attrs__.extensions_file_url.\
                         validator,
                         self.filemodel,
                         self.filemodel.__attrs_attrs__.extensions_file_url,
                         2)

    def test_validate_extensions_file_url_value_invalid_message(self):
        with self.assertRaises(ValueError) as error:
            self.filemodel.__attrs_attrs__.extensions_file_url.validator(
                self.filemodel,
                self.filemodel.__attrs_attrs__.extensions_file_url,
                -10)
        self.assertEqual(error.exception.__str__(),
                         f"{self.filemodel.__attrs_attrs__.extensions_file_url.name}" \
                         " must be string.")

    def test_get_size_in_bytes(self):

        bytes_test = FileModel('www', 0, 100, 'Bytes', 0, '-')

        self.assertEqual(bytes_test.get_size_in_bytes(), 100)

        kb_test = FileModel('www', 0, 100, 'KB', 0, '-')

        self.assertEqual(kb_test.get_size_in_bytes(), 100 * 1000)

        mb_test = FileModel('www', 0, 100, 'MB', 0, '-')

        self.assertEqual(mb_test.get_size_in_bytes(), 100 * 125000)


class AggregateModelTest(unittest.TestCase):

    def setUp(self):
        self.aggregate = Aggregate('extesion', 0, 0, 'Bytes', 0)

    def test_model(self):

        self.assertTrue(hasattr(self.aggregate.__attrs_attrs__, 'extension'))
        self.assertTrue(self.aggregate.__attrs_attrs__.extension.converter is str)
        self.assertTrue(self.aggregate.__attrs_attrs__.extension.type is str)
        # self.assertIsNotNone(self.aggregate.__attrs_attrs__.extension.validator)

        self.assertTrue(hasattr(self.aggregate.__attrs_attrs__, 'qty_lines'))
        self.assertTrue(
            self.aggregate.__attrs_attrs__.qty_lines.converter is int)
        self.assertTrue(self.aggregate.__attrs_attrs__.qty_lines.type is int)
        self.assertIsNotNone(
            self.aggregate.__attrs_attrs__.qty_lines.validator)

        self.assertTrue(hasattr(self.aggregate.__attrs_attrs__, 'size_files'))
        self.assertTrue(
            self.aggregate.__attrs_attrs__.size_files.converter is float)
        self.assertTrue(self.aggregate.__attrs_attrs__.size_files.type is float)
        self.assertIsNotNone(
            self.aggregate.__attrs_attrs__.size_files.validator)

        self.assertTrue(hasattr(self.aggregate.__attrs_attrs__, 'unit'))
        self.assertTrue(self.aggregate.__attrs_attrs__.unit.converter is str)
        self.assertTrue(self.aggregate.__attrs_attrs__.unit.type is str)
        # self.assertIsNotNone(self.aggregate.__attrs_attrs__.unit.validator)

    def test_validate_qty_lines_value_ok(self):
        self.aggregate.__attrs_attrs__.qty_lines.validator(
            self.aggregate,
            self.aggregate.__attrs_attrs__.qty_lines,
            10)

    def test_validate_qty_lines_value_invalid(self):
        self.\
            assertRaises(ValueError,
                         self.aggregate.__attrs_attrs__.qty_lines.validator,
                         self.aggregate,
                         self.aggregate.__attrs_attrs__.qty_lines,
                         -2)

    def test_validate_qty_lines_value_invalid_message(self):
        with self.assertRaises(ValueError) as error:
            self.aggregate.__attrs_attrs__.qty_lines.validator(
                self.aggregate,
                self.aggregate.__attrs_attrs__.qty_lines,
                -10)
        self.assertEqual(error.exception.__str__(),
                         f"{self.aggregate.__attrs_attrs__.qty_lines.name}" \
                         " must be bigger or equal to 0.")

    def test_validate_size_file_value_ok(self):
        self.aggregate.__attrs_attrs__.size_files.validator(
            self.aggregate,
            self.aggregate.__attrs_attrs__.size_files,
            10)

    def test_validate_size_file_value_invalid(self):
        self.\
            assertRaises(ValueError,
                         self.aggregate.__attrs_attrs__.size_files.validator,
                         self.aggregate,
                         self.aggregate.__attrs_attrs__.size_files,
                         -2)

    def test_validate_size_file_value_invalid_message(self):
        with self.assertRaises(ValueError) as error:
            self.aggregate.__attrs_attrs__.size_files.validator(
                self.aggregate,
                self.aggregate.__attrs_attrs__.size_files,
                -10)
        self.assertEqual(error.exception.__str__(),
                         f"{self.aggregate.__attrs_attrs__.size_files.name}" \
                         " must be bigger or equal to 0.")

    def test_get_row(self):
        total_lines = 100
        zero_lines = 0
        empty = Aggregate('extesion', 0, 0, 'Bytes', 0)

        self.assertListEqual(empty.get_row(total_lines),
                             ['extesion', '0 (0.0000 %)', 0])

        normal = Aggregate('py', 100, 10, 'Bytes', 0)

        self.assertListEqual(normal.get_row(total_lines),
                             ['py', '100 (100.0000 %)', 10.0])

        self.assertListEqual(normal.get_row(zero_lines),
                             ['py', '100 (0.0000 %)', 10.0])

