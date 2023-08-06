"""
This code defines a function which installs a given list of PIP packages.
"""

# Standard imports.
import subprocess

# Local constants.
DEFAULT_INTERNAL_PIP_COMMAND = "pip3"

#############
# FUNCTIONS #
#############

def install_dependency(
        package_string, internal_pip_command=DEFAULT_INTERNAL_PIP_COMMAND
    ):
    """ Install a PIP package from a given package string, e.g. "pytest",
    "pylint>=2.12.2", etc. """
    try:
        subprocess.run(
            [internal_pip_command, "install", package_string], check=True
        )
    except subprocess.CalledProcessError:
        return False
    return True

def install_dependencies(
        package_list, internal_pip_command=DEFAULT_INTERNAL_PIP_COMMAND
    ):
    """ As above, but for several packages. """
    for package_string in package_list:
        local_result = \
            install_dependency(
                package_string, internal_pip_command=internal_pip_command
            )
        if not local_result:
            return False
    return True

def install_apt_package(package_string, raise_error=True, quiet=False):
    """ Obviously, this will only work in a Debian-based system. """
    if not quiet:
        print(
            "I'm going to need superuser privileges to install "+
            package_string+
            "..."
        )
    try:
        subprocess.run(
            ["sudo", "apt-get", "install", package_string], check=True
        )
    except subprocess.CalledProcessError:
        if raise_error:
            raise
        return False
    return True

def install_apt_packages(package_strings, raise_error=True, quiet=False):
    """ An iterative version of the above. """
    if not quiet:
        print(
            "I'm going to need superuser privileges to install "+
            str(package_strings)+
            "..."
        )
    for package_string in package_strings:
        install_apt_package(package_string, raise_error=raise_error, quiet=True)
