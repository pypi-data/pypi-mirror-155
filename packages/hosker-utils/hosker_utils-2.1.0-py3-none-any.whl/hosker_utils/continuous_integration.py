"""
This code defines some useful functions when writing a minimal continuous
integration routine.
"""

# Standard imports.
import shutil
import subprocess
from glob import glob
from pathlib import Path

# Non-standard imports.
import pytest
from termcolor import colored

DEFAULT_PATH_TO_LINTER_RC = "pylintrc"
PATH_TO_BACKUP_LINTER_RC = \
    str(Path(__file__).parent/"backup_configs"/"backup_pylintrc")
DEFAULT_PATH_TO_TEST_INI = "pytest.ini"
PATH_TO_BACKUP_TEST_INI = \
    str(Path(__file__).parent/"backup_configs"/"backup_pytest.ini")

#############
# FUNCTIONS #
#############

def print_encased(message, symbol="#", print_color=None):
    """ Print the message encased in hashes. """
    message_line = symbol+" "+message+" "+symbol
    hashes = ""
    for _ in range(len(message_line)):
        hashes = hashes+symbol
    if print_color:
        print(colored(" ", print_color))
        print(colored(hashes, print_color))
        print(colored(message_line, print_color))
        print(colored(hashes, print_color))
        print(colored(" ", print_color))
    else:
        print(" ")
        print(hashes)
        print(message_line)
        print(hashes)
        print(" ")

def run_tests(path_to_test_ini=DEFAULT_PATH_TO_TEST_INI):
    """ Run PyTest. """
    if not Path(path_to_test_ini).exists():
        shutil.copy(PATH_TO_BACKUP_TEST_INI, path_to_test_ini)
    return_code = pytest.main()
    if return_code == 0:
        return True
    return False

def run_linter(path_to_linter_rc=DEFAULT_PATH_TO_LINTER_RC):
    """ Run PyLint on this repo. """
    if not Path(path_to_linter_rc).exists():
        shutil.copy(PATH_TO_BACKUP_LINTER_RC, path_to_linter_rc)
    source_file_paths = glob("**/*.py")
    arguments = ["pylint"]+source_file_paths
    try:
        subprocess.run(arguments, check=True)
    except subprocess.CalledProcessError:
        return False
    return True

def run_continuous_integration_no_print(
        lint=True, test=True, stop_on_failure=False
    ):
    """ Execute a minimal continuous integration routine. """
    lint_result, test_result = True, True
    if lint:
        lint_result = run_linter()
        if (not lint_result) and stop_on_failure:
            return False
    if test:
        test_result = run_tests()
        if (not test_result) and stop_on_failure:
            return False
    if lint_result and test_result:
        return True
    return False

def run_continuous_integration(lint=True, test=True, stop_on_failure=False):
    """ Run this file. """
    print_encased("Starting continuous integration routine...")
    result = \
        run_continuous_integration_no_print(
            lint=lint, test=test, stop_on_failure=stop_on_failure
        )
    if result:
        print_encased("Continuous integration: PASS", print_color="green")
    else:
        print_encased("Continuous integration: FAIL", print_color="red")
    return result
