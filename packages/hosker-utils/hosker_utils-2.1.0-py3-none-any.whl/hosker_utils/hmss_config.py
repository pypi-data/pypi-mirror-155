"""
This file lists some configurations for HMSS.
"""

# Standard imports.
from pathlib import Path

##################
# CONFIGURATIONS #
##################

# Components.
PATH_TO_HOME = Path.home()

# Defaults.
DEFAULT_EMAIL_ADDRESS = "tomdothosker@gmail.com"
DEFAULT_ENCODING = "utf-8"
DEFAULT_GIT_USERNAME = "tomhosker"
DEFAULT_OS = "ubuntu"
DEFAULT_PATH_TO_GIT_CREDENTIALS = str(PATH_TO_HOME/".git-credentials")
DEFAULT_PATH_TO_PAT = str(PATH_TO_HOME/"personal_access_token.txt")
DEFAULT_PATH_TO_WALLPAPER_DIR = str(PATH_TO_HOME/"hmss"/"wallpaper")
DEFAULT_PYTHON_VERSION = 3
DEFAULT_TARGET_DIR = PATH_TO_HOME
DEFAULT_PATH_TO_HMSS_CONFIG_FILE = str(DEFAULT_TARGET_DIR/"hmss_config.json")
CODE_INDENTATION = 4

# Command elements.
INTERNAL_PYTHON_COMMAND = "python3"
