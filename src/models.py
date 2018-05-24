# -*- coding: utf-8 -*-

import attr


@attr.s
class FileModel(object):
    url = attr.ib(type=str, converter=str)

    @url.validator
    def check(self, attribute, value):
        if value is None or isinstance(value, str) is False:
            raise ValueError(f"{attribute.name} must be string.")

    qty_lines = attr.ib(type=int, converter=int)

    @qty_lines.validator
    def check(self, attribute, value):
        if value < 0:
            raise ValueError(f"{attribute.name} must be bigger or equal to 0.")

    size_file = attr.ib(type=float, converter=float)

    @size_file.validator
    def check(self, attribute, value):
        if value < 0:
            raise ValueError(f"{attribute.name} must be bigger or equal to 0.")

    unit = attr.ib(type=str, converter=str)

    @unit.validator
    def check(self, attribute, value):
        valids_values = ["Bytes", "KB", "MB"]
        if value is None:
            raise ValueError(f"{attribute.name} must be string.")
        elif value not in valids_values and value != '-':
            msg = f"{attribute.name} must be {', '.join(valids_values)}."
            raise ValueError(msg)

    is_file = attr.ib(type=int, converter=int)

    @is_file.validator
    def check(self, attribute, value):
        if value < 0 or value > 1:
            raise ValueError(f"{attribute.name} must be 0 or 1.")

    extensions_file_url = attr.ib(type=str, converter=str)

    @extensions_file_url.validator
    def check(self, attribute, value):
        if isinstance(value, str) is False:
            raise ValueError(f"{attribute.name} must be string.")

    def get_size_in_bytes(self):
        if self.unit == 'Bytes':
            return self.size_file
        elif self.unit == 'KB':
            return self.size_file * 1000
        elif self.unit == 'MB':
            return self.size_file * 125000

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
