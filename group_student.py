"""
This module handles information regarding the groups grade sheet.
"""
from dataclasses import dataclass
from os import path
import csv
from logger import fail


@dataclass
class Student:
    """It contains information regarding a student."""
    group_id: str
    moodle_id: str
    mail: str
    grade: str
    full_name: str
    start_page: int
    num_pages: int


@dataclass
class Group:
    """It contains information regarding a group of students.

    All the students in a group have submitted the same assignment, and
    they receive the same grade.
    """
    group_id: str
    members: list[Student]
    grade: str
    start_page: int
    num_pages: int


def read_groups_csv(filename, header_config):
    """It reads the group gradesheet from the given filename in CSV format,
    and it returns a list of groups.

    The header_config param contains the names of the headers where the
    relevant information is to be found.
    """
    if not path.exists(filename):
        fail(f"{filename} not found")
    with open(filename, "r", newline="", encoding="utf-8-sig") as csvfile:
        rows = csv.reader(csvfile)
        header = next(rows)
        for column in [header_config.group_column, header_config.grade_column,
                  header_config.num_pages_column, header_config.mail_column]:
            if column not in header:
                fail(f"File {filename} does not contain a header called {column}")
        group_idx = header.index(header_config.group_column)
        grade_idx = header.index(header_config.grade_column)
        numpages_idx = header.index(header_config.num_pages_column)
        mail_idx = header.index(header_config.mail_column)
        result = []
        page_counter = 0
        for row in rows:
            mails = filter(lambda x: x != "", row[mail_idx:])
            num_pages = int(row[numpages_idx])
            students = map(lambda m: Student(group_id=row[group_idx], mail=m,
                                             moodle_id=None, grade=row[grade_idx], full_name=None,
                                             start_page=page_counter, num_pages=num_pages),
                           mails
                           )
            result.append(Group(group_id=row[group_idx], members=list(students),
                                grade=row[grade_idx],
                                start_page=page_counter, num_pages=num_pages))
            page_counter += num_pages
        return result


def build_students_map(groups):
    """Given a list of groups, it returns a dictionary of students that maps
    each student's email to its corresponding Student object"""
    result = {}
    for group in groups:
        for member in group.members:
            result[member.mail] = member
    return result
