"""
This module reads and manages configuration files.
"""

import configparser
from dataclasses import dataclass
from logger import fail


DEFAULT_CONFIG = """# This section specifies in which directory the separated PDF files will
# be created. Inside 'attachments_dir' a directory per user will be created

[Output]
attachments_dir = attachments

# PDF file containing the corrected assignments. This is the file that will
# be splitted

[MainPDF]
file_name = main.pdf

# The following section contains the information of the Moodle CSV Gradesheet
# that will be modified in order to put the grade of each student. This CSV is expected
# to have a header column, which will be used by split_and_grade to determine where
# to read the student's information and where to write the grade.
#
# file_name   : Name of the CSV file of the gradesheet
# id_column   : Header of the column that contains the student's Moodle ID. This is necessary to
#              create the directory of attachments corresponding to each student.
# mail_column : Header of the column that contain student's e-mail address. This is used to match
#               each entry with those of the Group CSV sheet.
# grade_column: Header of the column that contain the grades
# full_name_column: Header of the column that contain each student's full name. This is used to
#              create the directory of attachments.
# identifier_prefix: The Moodle ID in the gradesheet usually takes the form 'Participant3238724'. Since
#               we are interested only in the number, this option specifies the prefix that will be stripped
#               from this column in order to obtain each student's Moodle ID.       

[MoodleGradesheet]
file_name = HojaMoodle.csv
id_column = Identificador
mail_column = Dirección de correo
grade_column = Calificación
full_name_column = Nombre completo
identifier_prefix = Participante


# The following section contains the information of the Group gradesheet, also in CSV format.
# The first row is expected to be a header specifying the contents of each column.
# These columns have to be in the following order.
#
# IMPORTANT: The mail_column must be the last header in the grade sheet, since all the columns from
#            it are assumed to contain the e-mail addresses of the students corresponding to the
#            group.
#
# file_name: Name of the CSV file of the gradesheet.
# group_id_column: Header of the column that contain each group's ID
# grade_column: Header of the column containing the grade of each assignment
# num_pages_column: Header of the column containing the number of pages in the main PDF file corresponding
#                   to that group
# mail_column: Header of the column containing the e-mail addresses of the members of the group.

[GroupSheet]
file_name = Groups.csv
group_id_column = Grupo
grade_column = Calificacion
num_pages_column = NumPaginas
mail_column = Correos
"""


@dataclass
class HeaderConfig:
    """
    Header names of the group gradesheet.
    """
    group_column: str
    grade_column: str
    num_pages_column: str
    mail_column: str


@dataclass
class MoodleConfig:
    """
    Header names of the Moodle gradesheet
    """
    moodle_id_column: str
    mail_column: str
    grade_column: str
    full_name_column: str
    id_prefix: str


@dataclass
class Config:
    """
    Configuration options
    """
    group_filename: str
    moodle_filename: str
    header: HeaderConfig
    moodle: MoodleConfig
    attachments_dir: str
    main_pdf: str


def read_config_file(filename):
    """Reads the configuration from the given filename (in INI format).

    It returns a Config object. If a section is missing, exits with an error message.
    """
    parser = configparser.ConfigParser()
    parser.read(filename)
    _check_options(filename, parser)
    return Config(
        group_filename=parser["GroupSheet"]["file_name"],
        moodle_filename=parser["MoodleGradesheet"]["file_name"],
        header=HeaderConfig(
            group_column=parser["GroupSheet"]["group_id_column"],
            grade_column=parser["GroupSheet"]["grade_column"],
            num_pages_column=parser["GroupSheet"]["num_pages_column"],
            mail_column=parser["GroupSheet"]["mail_column"]
        ),
        moodle=MoodleConfig(
            moodle_id_column=parser["MoodleGradesheet"]["id_column"],
            mail_column=parser["MoodleGradesheet"]["mail_column"],
            grade_column=parser["MoodleGradesheet"]["grade_column"],
            full_name_column=parser["MoodleGradesheet"]["full_name_column"],
            id_prefix=parser["MoodleGradesheet"]["identifier_prefix"]
        ),
        attachments_dir=parser["Output"]["attachments_dir"],
        main_pdf=parser["MainPDF"]["file_name"]
    )


def _check_options(filename, parser):
    # It checks whether all the mandatory sections and options are present
    # in the INI file
    sections = {"Output": ["attachments_dir"],
                "MainPDF": ["file_name"],
                "MoodleGradesheet": ["file_name", "id_column", "mail_column", "grade_column",
                                     "full_name_column", "identifier_prefix"],
                "GroupSheet": ["file_name", "group_id_column", "grade_column",
                               "num_pages_column", "mail_column"]}
    for section, options in sections.items():
        if section not in parser:
            fail(f"Section [{section}] not found in {filename}")
        for option in options:
            if option not in parser[section]:
                fail(
                    f"Option '{option}' not found in section [{section}] of {filename}")


def create_default_config_file(filename):
    """It creates a file with the default configuration template."""
    with open(filename, "w", encoding="utf8") as file:
        file.write(DEFAULT_CONFIG)
