"""
This code defines the script required by setuptools.
"""

# Non-standard imports.
from setuptools import setup

# Local constants.
PACKAGE_NAME = "hosker_utils"
VERSION = "2.0.0"
DESCRIPTION = "General utility functions"
GIT_URL_STEM = "https://github.com/tomhosker"
AUTHOR = "Tom Hosker"
AUTHOR_EMAIL = "tomdothosker@gmail.com"
SCRIPT_PATHS = ["scripts/install_hmss"]
INSTALL_REQUIRES = (
    "pylint>=2.12.2", "pytest>=7.1.2", "pytest-cov", "termcolor"
)

###################################
# THIS IS WHERE THE MAGIC HAPPENS #
###################################

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=GIT_URL_STEM+"/"+PACKAGE_NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    package_dir={ PACKAGE_NAME: "source" },
    packages=[PACKAGE_NAME],
    scripts=SCRIPT_PATHS,
    install_requires=INSTALL_REQUIRES
)
