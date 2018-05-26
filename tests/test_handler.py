# -*- coding: utf-8 -*-

import unittest
import os

from prettytable import PrettyTable
from treelib import Node, Tree

from src.app import Handler
from src.models import FileModel, Aggregate


class HandlerTest(unittest.TestCase):

    def setUp(self):
        self.handler = Handler()

    def test_open_input_txt_file(self):
        file = os.path.join(os.path.dirname(__file__), 'artifacts/input.txt')
        self.assertListEqual(
            self.handler.open_input_txt_file(file),
            ['https://github.com/linha/um', 'https://github.com/linha/dois'])

    def test_open_input_txt_empty_file(self):
        file = os.path.join(os.path.dirname(__file__),
                            'artifacts/empty_input.txt')
        self.assertListEqual(
            self.handler.open_input_txt_file(file), [])

    def test_clean_workspace_with_existing_file(self):
        path = os.path.join(os.path.dirname(__file__), 'artifacts/newfile.txt')
        with open(path, 'w') as f:
            f.write('tests')

        self.assertTrue(os.path.exists(path))
        self.handler.clean_workspace(path)
        self.assertFalse(os.path.exists(path))

    def test_clean_workspace_without_existing_file(self):
        path = os.path.join(os.path.dirname(__file__),
                            'artifacts/no_existing_file.txt')

        self.assertFalse(os.path.exists(path))
        self.handler.clean_workspace(path)

    def test_create_output_folder_with_existing_folder(self):
        path = os.path.join(os.path.dirname(__file__),
                            'artifacts/output')
        if not os.path.exists(path):
            os.mkdir(path)
        self.assertTrue(os.path.exists(path))
        self.handler.create_output_folder()

    def test_create_output_folder_without_existing_folder(self):
        path = os.path.join(os.path.dirname(__file__),
                            'artifacts/output')
        if os.path.exists(path):
            os.rmdir(path)
        self.assertFalse(os.path.exists(path))
        self.handler.create_output_folder()

    def test_read_csv_file_with_existing_file(self):
        path = os.path.join(os.path.dirname(__file__),
                            'artifacts/crawled_data.csv')

        file_one = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace/blob/master/tests/Tests.elm",
            132,
            4.21,
            'KB',
            1,
            'elm')

        file_two = FileModel(
            "Bernardoow/study_of_attrs_and_tests/blob/master/src/test_model.py",
            73,
            2.62,
            'KB',
            1,
            'py')

        self.assertDictEqual(self.handler.read_csv_file(path),
                             {'Bernardoow/Elm-SqlAlchemy-Replace': [file_one],
                              'Bernardoow/study_of_attrs_and_tests': [file_two]
                              })

    def test_read_csv_file_without_existing_file(self):
        path = os.path.join(os.path.dirname(__file__),
                            'artifacts/no_existing_crawled_data.csv')
        self.assertDictEqual(self.handler.read_csv_file(path), {})

    def test_read_csv_file_with_empty_existing_file(self):
        path = os.path.join(os.path.dirname(__file__),
                            'artifacts/empty_crawled_data.csv')
        self.assertDictEqual(self.handler.read_csv_file(path), {})

    def test_summarize_data(self):
        file_one = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace/blob/master/tests/Tests.elm",
            132,
            4.21,
            'KB',
            1,
            'elm')

        file_two = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace/blob/master/src/test_model.py",
            73,
            2.62,
            'KB',
            1,
            'py')

        file_three = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace/blob/master/tests/Tests.elm",
            132,
            4.21,
            'KB',
            1,
            'elm')

        file_four = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace/blob/master/src/test_model.py",
            73,
            2.62,
            'KB',
            1,
            'py')

        qty_lines, size_files, pretty_table = self.handler.summarize_data([
            file_one, file_two, file_three, file_four
        ])

        agg_one = Aggregate('elm', 264, 8.42, 'Bytes', 0)
        agg_two = Aggregate('py', 146, 5.24, 'Bytes', 0)

        pretty_table_check = PrettyTable()
        pretty_table_check.field_names = ["Extension", "Lines", "Size"]
        pretty_table_check.add_row(agg_one.get_row(410))
        pretty_table_check.add_row(agg_two.get_row(410))

        self.assertEqual(qty_lines, 410)
        self.assertEqual(size_files, 13.66)
        self.assertEqual(pretty_table, pretty_table_check.get_string())

    def test_create_tree(self):

        file_one = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace/blob/master/tests/Tests.elm",
            132,
            4.21,
            'KB',
            1,
            'elm')

        file_two = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace/blob/master/src/test_model.py",
            73,
            2.62,
            'KB',
            1,
            'py')

        file_three = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace/blob/master/readme.md",
            73,
            2.62,
            'Bytes',
            1,
            'md')

        tree_response = self.handler.create_tree([
            file_one,
            file_two,
            file_three
        ])

        tree = Tree()
        tree.create_node("Bernardoow", "Bernardoow")  # root node
        tree.create_node("Elm-SqlAlchemy-Replace", "Elm-SqlAlchemy-Replace", parent="Bernardoow")
        tree.create_node("blob", "blob", parent="Elm-SqlAlchemy-Replace")
        tree.create_node("master", "master", parent="blob")
        tree.create_node("readme.md", "readme.md", parent="master")
        tree.create_node("tests", "tests", parent="master")
        tree.create_node("Tests.elm", "Tests.elm", parent="tests")
        tree.create_node("src", "src", parent="master")
        tree.create_node("test_model.py", "test_model.py", parent="src")

        self.assertEqual(tree_response.to_json(), tree.to_json())

    def test_create_tree_with_tree_party(self):

        file_zero = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace",
            132,
            4.21,
            'KB',
            1,
            'elm')

        file_one = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace/blob/master/tests/Tests.elm",
            132,
            4.21,
            'KB',
            1,
            'elm')

        file_two = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace/blob/master/src/test_model.py",
            73,
            2.62,
            'KB',
            1,
            'py')

        file_three = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace/blob/master/readme.md",
            73,
            2.62,
            'Bytes',
            1,
            'md')

        file_four = FileModel(
            "Bernardoow/Elm-SqlAlchemy-Replace/tree/teste",
            73,
            2.62,
            'Bytes',
            0,
            'md')

        tree_response = self.handler.create_tree([
            file_zero,
            file_one,
            file_two,
            file_three,
            file_four
        ])

        tree = Tree()
        tree.create_node("Bernardoow", "Bernardoow")
        tree.create_node("Elm-SqlAlchemy-Replace", "Elm-SqlAlchemy-Replace",
                         parent="Bernardoow")
        tree.create_node("blob", "blob", parent="Elm-SqlAlchemy-Replace")
        tree.create_node("master", "master", parent="blob")
        tree.create_node("readme.md", "readme.md", parent="master")
        tree.create_node("tests", "tests", parent="master")
        tree.create_node("Tests.elm", "Tests.elm", parent="tests")
        tree.create_node("src", "src", parent="master")
        tree.create_node("test_model.py", "test_model.py", parent="src")

        self.assertEqual(tree_response.to_json(), tree.to_json())

    def test_do_crawler(self):
        file = os.path.join(os.path.dirname(__file__),
                            'artifacts/crawled_data_do_crawler.csv')

        handler = Handler()
        handler.do_crawler(
            ['https://github.com/Bernardoow/study_of_attrs_and_tests'],
            file)

        data = """url,qty_lines,size_files,unit,is_file,extensions_file_url
            Bernardoow/study_of_attrs_and_tests,0,0,-,0,-
            Bernardoow/study_of_attrs_and_tests/blob/master/setup.py,8,160,Bytes,1,py
            Bernardoow/study_of_attrs_and_tests/tree/master/src,0,0,-,0,-
            Bernardoow/study_of_attrs_and_tests/blob/master/Pipfile.lock,232,12.5,KB,1,lock
            Bernardoow/study_of_attrs_and_tests/blob/master/Pipfile,22,195,Bytes,1,com/Bernardoow/study_of_attrs_and_tests/blob/master/Pipfile
            Bernardoow/study_of_attrs_and_tests/blob/master/.gitignore,105,1.17,KB,1,gitignore
            Bernardoow/study_of_attrs_and_tests/blob/master/LICENSE,22,1.05,KB,1,com/Bernardoow/study_of_attrs_and_tests/blob/master/LICENSE
            Bernardoow/study_of_attrs_and_tests/blob/master/src/models.py,21,450,Bytes,1,py
            Bernardoow/study_of_attrs_and_tests/blob/master/.travis.yml,16,193,Bytes,1,yml
            Bernardoow/study_of_attrs_and_tests/blob/master/readme.md,8,796,Bytes,1,md
            Bernardoow/study_of_attrs_and_tests/tree/master/test,0,0,-,0,-
            Bernardoow/study_of_attrs_and_tests/blob/master/src/__init__.py,0,0,Bytes,1,py
            Bernardoow/study_of_attrs_and_tests/blob/master/test/__init__.py,0,0,Bytes,1,py
            Bernardoow/study_of_attrs_and_tests/blob/master/test/test_model.py,72,2.61,KB,1,py"""

        data = [row.strip() for row in data.split("\n")]
        with open(file, 'r') as f:
            data_crawled = [row.strip() for row in f.readlines()]

        self.assertListEqual(sorted(data_crawled), sorted(data))
