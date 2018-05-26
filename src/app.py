# -*- coding: utf-8 -*-
import csv
import os

from treelib import Node, Tree
from prettytable import PrettyTable
from scrapy.crawler import CrawlerProcess

from src.models import FileModel, Aggregate
from src.spiders.github import GithubSpider


class Handler(object):

    def read_csv_file(self, filename):
        files_info = {}
        try:
            with open(filename, newline='') as csvfile:
                rows = csv.reader(csvfile, delimiter=',')
                next(rows, None)
                for row in rows:
                    file_model = FileModel(*row)

                    key = "/".join(
                        file_model.url.split("/")[:2]
                    )
                    if key not in files_info:
                        files_info[key] = []
                    files_info[key].append(file_model)
        except FileNotFoundError:
            pass

        return files_info

    def summarize_data(self, files):
        extesions = {}
        qty_lines = 0
        size_files = 0.0
        for file in files:

            pieces = file.url.split(".")

            if len(pieces) == 1:
                extesion = 'other'
            else:
                extesion = pieces[-1].lower()

            if extesion not in extesions:
                extesions[extesion] = Aggregate(extesion, 0, 0, 'Bytes', 0)

            agg = extesions[extesion]
            agg.qty_lines += int(file.qty_lines)
            qty_lines += int(file.qty_lines)
            agg.size_files += float(file.size_file)
            size_files += float(file.size_file)

            extesions[extesion] = agg

        pretty_table = PrettyTable()

        pretty_table.field_names = ["Extension", "Lines", "Size"]

        for key, extesion in sorted(extesions.items()):
            pretty_table.add_row(extesion.get_row(qty_lines))

        return qty_lines, size_files, pretty_table.get_string()

    def create_tree(self, files):
        tree = Tree()
        root = files[0]
        tree.create_node(root.url.split("/")[0], root.url.split("/")[0])
        for item in files:
            if not tree.contains(item.url):
                pieces = item.url.split("/")
                for index, path in enumerate(pieces, 1):
                    if not tree.contains("/".join(pieces[:index])):
                        tree.create_node(path, "/".join(pieces[:index]),
                                         parent="/".join(pieces[:index - 1]))

            # if not tree.contains("/".join(pieces)):
            #     tree.create_node(pieces[-1], "/".join(pieces),
            #                      parent="/".join(pieces[:-2]))

        if tree.contains(f'{root.url}/tree'):
            tree.remove_node(f'{root.url}/tree')

        return tree



    def open_input_txt_file(self, path):
        with open(path) as f:
            break_line = "\n"
            return [f"https://github.com/{line.replace(break_line, '')}"
                    for line in f.readlines()]

    def clean_workspace(self, path):
        try:
            os.remove(path)
        except OSError:
            pass

    def create_output_folder(self):
        if not os.path.exists('./output'):
            os.makedirs('./output')

    def do_crawler(self, repositories_lists, path_file_data_crawled):
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'csv',
            'FEED_URI': f'{path_file_data_crawled}',
            'FEED_STORE_EMPTY': True,
            'DOWNLOAD_TIMEOUT': "15",
            'LOG_ENABLED': False,
        })

        self.clean_workspace(path_file_data_crawled)

        process.crawl(GithubSpider, start_urls=repositories_lists)
        process.start()

    def do_test(self):
        self.create_output_folder()
        repositories_lists = self.open_input_txt_file('./src/input.txt')
        self.do_crawler(repositories_lists, './result.csv')
        repositories_files = self.read_csv_file('./result.csv')

        for repository, lista in repositories_files.items():
            qty_lines, size_files, table = self.summarize_data(lista)
            tree = self.create_tree(lista)
            file_path = f'./output/{repository.replace("/", "_")}.txt'
            with open(file_path, 'w') as f:
                f.write(repository + "\n")
                f.write(f"Total de linhas: {qty_lines}." + "\n")
                f.write(f"Tamanho total: {size_files} Bytes." + "\n")
                f.write(table)
                f.write("\n")

            tree.save2file(file_path)