import csv
import sys
from pathlib import Path
from typing import List

import numpy as np


class TableWriter:
    """Class description."""

    def __init__(self):
        """
        Initialisation of the class.
        """

        self.header: List[str] = []
        self.footer: List[str] = []
        self.body: List[List[str]] = []
        self.border: bool = True
        self.alignment: str or List[str] = ["<"]
        self.uppercased: bool = False
        self.column_separator: str = "|"
        self.center_separator: str = "+"

    @property
    def column_count(self):
        if len(self.header) == 0 and len(self.body) == 0:
            return 0

        if len(self.header) == 0:
            return len(self.body[0])

        if len(self.body) == 0:
            return len(self.header)

        return len(self.body[0])

    def set_uppercased(self, state: bool):
        self.uppercased = state

    def set_header(self, header: List[str]):
        self.header = header

    def set_footer(self, footer: List[str]):
        self.footer = footer

    def set_border(self, state: bool):
        self.border = state

    def set_alignment(self, alignment: str or List[str]):
        def check_sign(sign: str):
            if sign in ["<", "left", "l"]:
                return ["<"]
            elif sign in [">", "right", "r"]:
                return [">"]
            elif sign in ["^", "center", "c"]:
                return ["^"]
            else:
                print("Unkown alignment option")
                return ["<"]

        if isinstance(alignment, str):
            self.alignment = check_sign(alignment)
        else:
            self.alignment = []
            for sign in alignment:
                self.alignment.append(check_sign(sign)[0])

    def set_center_separator(self, separator: str):
        self.center_separator = separator

    def set_column_separator(self, separator: str):
        self.column_separator = separator

    def from_csv(
        self, filename: Path, header: bool = False, footer: bool = False, sep: str = ","
    ):
        rows: List[str] = []

        with open(filename, "r") as f:
            csvreader = csv.reader(f, delimiter=sep)

            rows = [row for row in csvreader]

        if header:
            self.set_header(rows[0])
            rows = rows[1:]

        if footer:
            self.set_footer(rows[-1])
            rows = rows[:-1]

        for row in rows:
            self.append(row)

    def format_title(self, text: str):
        if self.uppercased:
            return text.upper()
        else:
            return text

    def reset_header(self):
        self.header = []

    def reset_footer(self):
        self.footer = []

    def reset_body(self):
        self.body = []

    def reset_content(self):
        self.reset_header()
        self.reset_body()
        self.reset_footer()

    def append(self, line: List[str]):
        if self.column_count != 0 and len(line) != self.column_count:
            raise ValueError("Column count not consistant")

        self.body.append(line)

    def append_bulk(self, data: List[List[str]]):
        for line in data:
            self.append(line)

    def render(self, file=sys.stdout):
        self.file = file
        widths = self.get_columns_widths()

        self.eprint(self.separation_line(True))

        if len(self.alignment) == 1:
            self.alignment = self.alignment * self.column_count

        # header
        if self.header:
            formatted_header = [
                f" {self.format_title(text):{align}{width}s} "
                for text, width, align in zip(self.header, widths, self.alignment)
            ]
            formatted_header = f"{self.column_separator.join(formatted_header)}"
            if self.border:
                formatted_header = (
                    f"{self.column_separator}{formatted_header}{self.column_separator}"
                )
            self.eprint(formatted_header)

            line = self.separation_line()
            self.eprint(line)

        # body
        for line in self.body:
            formatted_line = [
                f" {text:{align}{width}s} "
                for text, width, align in zip(line, widths, self.alignment)
            ]
            formatted_line = f"{self.column_separator.join(formatted_line)}"

            if self.border:
                formatted_line = (
                    f"{self.column_separator}{formatted_line}{self.column_separator}"
                )

            self.eprint(formatted_line)

        # footer
        if self.footer:
            formatted_footer = [
                f" {self.format_title(text):{align}{width}s} "
                for text, width, align in zip(self.footer, widths, self.alignment)
            ]
            formatted_footer = f"{' '.join(formatted_footer)}"
            if self.border:
                formatted_footer = f" {formatted_footer} "
            self.eprint(self.separation_line())
            self.eprint(formatted_footer)
            if self.border:
                self.eprint(self.footer_line())
        else:
            self.eprint(self.separation_line(True))

    def footer_line(self) -> str:
        widths = self.get_columns_widths()
        segments = []
        for idx, (text, width) in enumerate(zip(self.footer, widths)):
            if text:
                segments.append(f"{self.center_separator}{'-' * (width + 2)}")
                if (
                    idx + 1 < self.column_count and not self.footer[idx + 1]
                ) or idx + 1 == self.column_count:
                    segments.append(self.center_separator)
            else:
                segments.append(f" {' ' * (width + 2)}")

        line = "".join(segments)
        return line

    def separation_line(self, ext: bool = False) -> str:
        widths = self.get_columns_widths()
        segments = ["-" * (width + 2) for width in widths]

        line = self.center_separator.join(segments)
        if self.border and ext:
            line = f"{self.center_separator}{line}{self.center_separator}"

        if not self.border and ext:
            return

        if not ext and self.border:
            return f"{self.center_separator}{line}{self.center_separator}"

        if not ext and not self.border:
            return f"{line}"

        return line

    def eprint(self, *args, **kwargs):
        if args[0] == None:
            return

        print(*args, file=self.file, **kwargs)

    def get_columns_widths(self):
        widths_array = []
        widths_array.extend([len(text) for line in self.body for text in line])

        if self.header:
            widths_array.extend([len(text) for text in self.header])
        if self.footer:
            widths_array.extend([len(text) for text in self.footer])

        widths_array = np.array(widths_array).reshape((-1, self.column_count))

        return widths_array.max(axis=0)
