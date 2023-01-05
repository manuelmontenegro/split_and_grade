"""
This module provides functions for reading and writing Moodle gradesheets in CSV format.
"""
import csv
from os import path
from logger import fail


def read_moodle_csv(filename, moodle_config):
    """It reads a Moodle gradesheet in CSV format and returns a list of rows."""
    if not path.exists(filename):
        fail(f"{filename} not found")
    with open(filename, "r", newline="", encoding="utf8") as csvfile:
        rows = csv.reader(csvfile)
        result = list(rows)
        _check_headers(filename, result[0], moodle_config)
        return result


def write_moodle_csv(filename, rows):
    """Given a list of rows, writes it into the given filename in CSV format."""
    with open(filename, "w", newline="", encoding="utf8") as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)


def _check_headers(filename, header, moodle_config):
    """It checks whether the given header contains all the columns specified
    in the configuration file"""
    for column in [moodle_config.moodle_id_column, moodle_config.mail_column,
                   moodle_config.grade_column, moodle_config.full_name_column]:
        if column not in header:
            fail(f"File {filename} does not contain a header called {column}")
