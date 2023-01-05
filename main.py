"""
Main module
"""

from os import path
from logger import log, log_warning
from configuration import read_config_file, create_default_config_file
from group_student import read_groups_csv, build_students_map
from splitter import write_pdf_users
from moodle_gradesheet import read_moodle_csv, write_moodle_csv

CONFIG_FILENAME = "split_and_grade.ini"


def _complete_student_info_from_moodle(students, moodle_csv, moodle_config):
    # Given a list of students and the Moodle grade sheet, it fills in the
    # full name of the student and its Moodle identifier.
    moodle_id_idx = moodle_csv[0].index(moodle_config.moodle_id_column)
    full_name_idx = moodle_csv[0].index(moodle_config.full_name_column)
    mail_idx = moodle_csv[0].index(moodle_config.mail_column)
    not_found = []
    for row in moodle_csv[1:]:
        mail = row[mail_idx]
        if mail not in students:
            not_found.append(mail)
        else:
            students[mail].moodle_id = row[moodle_id_idx].removeprefix(
                moodle_config.id_prefix)
            students[mail].full_name = row[full_name_idx]
    return not_found


def _fill_in_grade(moodle_csv, students_map, moodle_config):
    mail_idx = moodle_csv[0].index(moodle_config.mail_column)
    grade_idx = moodle_csv[0].index(moodle_config.grade_column)
    for row in moodle_csv[1:]:
        mail = row[mail_idx]
        if mail in students_map:
            row[grade_idx] = students_map[mail].grade


def split_and_grade(configuration):
    """Main function. Given a configuration object, it splits the main PDF file into
    parts, each one corresponding to a group submission. It also fills in the Moodle
    gradesheet from the information given in the group gradesheet.
    """
    groups = read_groups_csv(configuration.group_filename, configuration.header)
    moodle_csv = read_moodle_csv(configuration.moodle_filename, configuration.moodle)
    students_map = build_students_map(groups)
    unused = _complete_student_info_from_moodle(
        students_map, moodle_csv, configuration.moodle)
    _fill_in_grade(moodle_csv, students_map, configuration.moodle)
    write_pdf_users(students_map, configuration.attachments_dir, configuration.main_pdf)
    log(f"Writing grades in {configuration.moodle_filename}")
    write_moodle_csv(configuration.moodle_filename, moodle_csv)

    for mail in unused:
        log_warning(f"{mail} does not appear in {configuration.group_filename}")
    for mail, student in students_map.items():
        if student.moodle_id is None:
            log_warning(f"{mail} does not appear in {configuration.moodle_filename}")


if __name__ == "__main__":
    if path.exists(CONFIG_FILENAME):
        config = read_config_file(CONFIG_FILENAME)
        split_and_grade(config)
    else:
        create_default_config_file(CONFIG_FILENAME)
        log(f"{CONFIG_FILENAME} created. Modify it and run again.")
