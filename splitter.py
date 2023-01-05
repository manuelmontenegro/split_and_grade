"""
This module extracts the pages of the main PDF corresponding to each group's submission.
"""
from os import path, makedirs
from pypdf import PdfWriter
from logger import log


def write_pdf_users(students, output_dir, main_pdf):
    """
    It generates a directory with the PDF feedback corresponding to each student.
    """
    for student in students.values():
        _write_pdf_user(student, output_dir, main_pdf)


def _write_pdf_user(student, output_dir, main_pdf):
    user_dir_name = f"{student.full_name}_{student.moodle_id}_assignsubmission_file_"
    file_name = f"{student.group_id}.pdf"
    full_user_dir = path.join(output_dir, user_dir_name)
    full_file_name = path.join(full_user_dir, file_name)
    makedirs(full_user_dir, exist_ok=True)
    log(f"Creating file {full_file_name}")
    with open(main_pdf, "rb") as input_pdf:
        writer = PdfWriter()
        writer.append(fileobj=input_pdf, pages=(student.start_page,
                      student.start_page + student.num_pages))
        writer.write(full_file_name)
        writer.close()
