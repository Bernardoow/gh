# -*- coding: utf-8 -*-

import attr

@attr.s
class FileModel(object):
    url = attr.ib()
    qty_lines = attr.ib()
    size_file = attr.ib()
    unit = attr.ib()
    is_file = attr.ib()
    extensions_file_url = attr.ib()

    def get_size_in_bytes(self):
        if self.unit == 'Bytes':
            return self.size_files
        elif self.unit == 'KB':
            return self.size_files * 1000
        elif self.unit == 'MB':
            return self.size_files * 125000

@attr.s
class Aggregate(object):
    extension = attr.ib()
    qty_lines = attr.ib()
    size_files = attr.ib()
    unit = attr.ib()
    percent_lines = attr.ib()

    def get_row(self, qty_lines_total):
        try:
            percent_lines = self.qty_lines / qty_lines_total * 100
        except ZeroDivisionError:
            percent_lines = 0

        return [
            self.extension,
            f"{self.qty_lines} ({percent_lines:.4f} %)",
            self.size_files
        ]
