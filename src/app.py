# -*- coding: utf-8 -*-
import csv

from treelib import Node, Tree
from prettytable import PrettyTable

from models import FileModel, Aggregate


class Handler(object):
    def read_csv_file(self, filename): # str-> list[str]
        files_info = []
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            cabecalho = 0
            for row in spamreader:
                if 1 == cabecalho:
                    files_info.append(FileModel(*row))
                else:
                    cabecalho = 1

        return files_info

    def summarize_data(self, files):
        extesions = {}
        qty_lines = 0
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

            extesions[extesion] = agg

        pretty_table = PrettyTable()

        pretty_table.field_names = ["Extension", "Lines", "Size"]

        for key, extesion in sorted(extesions.items()):
            pretty_table.add_row(extesion.get_row(qty_lines))

        return pretty_table.get_string()

    def create_tree(self, files):
        tree = Tree()
        root = files[0]
        tree.create_node(root.url.split("/")[0], root.url.split("/")[0])
        for item in files:
            pieces = item.url.split("/")
            if not tree.contains("/".join(pieces[:-2])):
                for index, path in enumerate(pieces, 1):
                    if not tree.contains("/".join(pieces[:index])):
                        tree.create_node(path, "/".join(pieces[:index]),
                                         parent="/".join(pieces[:index - 1]))

            if not tree.contains("/".join(pieces)):
                tree.create_node(pieces[-1], "/".join(pieces),
                                 parent="/".join(pieces[:-2]))

        tree.remove_node(f'{root.url}/tree')

        return tree
