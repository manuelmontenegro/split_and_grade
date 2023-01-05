"""
Simple module for showing logging messages, warnings and errors.
"""
import sys

COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
END_COLOR = '\033[0m'


def log(message):
    """It logs the given message."""
    print(f"{COLOR_GREEN}*{END_COLOR} {message}")


def log_warning(message):
    """It prints the given message as a warning."""
    print(f"{COLOR_YELLOW}* Warning:{END_COLOR} {message}")


def fail(message):
    """It prints the given message as a fatal error, and aborts the program."""
    print(f"{COLOR_RED}* Fatal:{END_COLOR} {message}")
    sys.exit(1)
