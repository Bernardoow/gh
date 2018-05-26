# -*- coding: utf-8 -*-

import unittest
import os

from src.spiders.github import GithubSpider
from tests.helpers import fake_response_from_file


class GHSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = GithubSpider()

    def test_parse_with_executable(self):
        file = os.path.join(os.path.dirname(__file__),
                            'artifacts/gh_info_with_executeble_file.html')

        url = "https://github.com/tuxrulez/binarios/blob/master/satelite2"

        results = self.spider.parse(
            fake_response_from_file(
                file,
                url=url))

        results = list(results)

        data = {'url': url.replace("https://github.com/", ""),
                'qty_lines': '13',
                'size_files': '705',
                'unit': 'Bytes',
                'is_file': 1,
                'extensions_file_url': 'satelite2'}

        self.assertEqual(len(results), 1)
        self.assertDictEqual(results[0], data)

    def test_parse_without_lines(self):
        file = os.path.join(os.path.dirname(__file__),
                            'artifacts/gh_info_without_lines.html')

        url = "https://github.com/getlantern/lantern-binaries/blob/master"
        url += "/lantern-installer-3.0.1.dmg"

        results = self.spider.parse(
            fake_response_from_file(
                file,
                url=url))

        results = list(results)

        data = {'url': url.replace("https://github.com/", ""),
                'qty_lines': 0,
                'size_files': '4.74',
                'unit': 'MB',
                'is_file': 1,
                'extensions_file_url': 'dmg'}

        self.assertEqual(len(results), 1)
        self.assertDictEqual(results[0], data)

    def test_parse_figure(self):
        file = os.path.join(os.path.dirname(__file__),
                            'artifacts/gh_info_figure.html')

        url = "https://github.com/ResidentMario/geoplot/blob/master"
        url += "/figures/dc-street-network.png"

        results = self.spider.parse(
            fake_response_from_file(
                file,
                url=url))

        results = list(results)

        data = {'url': url.replace("https://github.com/", ""),
                'qty_lines': 0,
                'size_files': '109',
                'unit': 'KB',
                'is_file': 1,
                'extensions_file_url': 'png'}

        self.assertEqual(len(results), 1)
        self.assertDictEqual(results[0], data)

    def test_parse_folder(self):
        file = os.path.join(os.path.dirname(__file__),
                            'artifacts/gh_folder.html')

        url = "https://github.com/Bernardoow/study_of_attrs_and_tests/tree"
        url += "/master/src"

        results = self.spider.parse(
            fake_response_from_file(
                file,
                url=url))

        results = list(results)

        data = {'url': url.replace("https://github.com/", ""),
                'qty_lines': 0,
                'size_files': 0,
                'unit': '-',
                'is_file': 0,
                'extensions_file_url': '-'}

        self.assertEqual(len(results), 3)
        self.assertDictEqual(results[0], data)
