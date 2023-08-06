"""
This code defines a class which installs the various packages and repositories
required on this computer.
"""

# Standard imports.
import contextlib
import json
import os
import shutil
import subprocess
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

# Local imports.
from .git_credentials import set_up_git_credentials
from .hmss_config import (
    DEFAULT_PATH_TO_GIT_CREDENTIALS,
    DEFAULT_PATH_TO_PAT,
    DEFAULT_GIT_USERNAME,
    DEFAULT_EMAIL_ADDRESS,
    DEFAULT_PATH_TO_HMSS_CONFIG_FILE,
    INTERNAL_PYTHON_COMMAND,
    CODE_INDENTATION
)
from .install_dependencies import install_dependency

# Local constants.
DEFAULT_OS = "ubuntu"
DEFAULT_TARGET_DIR = str(Path.home())
DEFAULT_PATH_TO_WALLPAPER_DIR = str(Path(__file__).parent/"wallpaper")
DEFAULT_HMSS_ARGUMENT_DICT = {
    "this_os": DEFAULT_OS,
    "target_dir": DEFAULT_TARGET_DIR,
    "thunderbird_num": None,
    "path_to_git_credentials": DEFAULT_PATH_TO_GIT_CREDENTIALS,
    "path_to_pat": DEFAULT_PATH_TO_PAT,
    "git_username": DEFAULT_GIT_USERNAME,
    "email_address": DEFAULT_EMAIL_ADDRESS,
    "path_to_wallpaper_dir": DEFAULT_PATH_TO_WALLPAPER_DIR,
    "test_run": False,
    "show_output": False,
    "minimal": True
}

##############
# MAIN CLASS #
##############

@dataclass
class HMSoftwareInstaller:
    """ The class in question. """
    # Fields
    this_os: str = DEFAULT_OS
    target_dir: str = DEFAULT_TARGET_DIR
    thunderbird_num: int = None
    path_to_git_credentials: str = DEFAULT_PATH_TO_GIT_CREDENTIALS
    path_to_pat: str = DEFAULT_PATH_TO_PAT
    git_username: str = DEFAULT_GIT_USERNAME
    email_address: str = DEFAULT_EMAIL_ADDRESS
    path_to_wallpaper_dir: str = DEFAULT_PATH_TO_WALLPAPER_DIR
    test_run: bool = False
    show_output: bool = False
    minimal: bool = True
    failure_log: list = field(default_factory=list)

    # Class attributes.
    CHROME_DEB: ClassVar[str] = "google-chrome-stable_current_amd64.deb"
    CHROME_STEM: ClassVar[str] = "https://dl.google.com/linux/direct/"
    EXPECTED_PATH_TO_GOOGLE_CHROME_COMMAND: ClassVar[str] = \
        "/usr/bin/google-chrome"
    GIT_URL_STEM: ClassVar[str] = "https://github.com/"
    MISSING_FROM_CHROME: ClassVar[tuple] = ("eog", "nautilus")
    OTHER_THIRD_PARTY: ClassVar[tuple] = ("gedit-plugins", "inkscape")
    SUPPORTED_OSS: ClassVar[set] = {
        "ubuntu", "chrome-os", "raspian", "linux-based"
    }
    WALLPAPER_STEM: ClassVar[str] = "wallpaper_t"
    WALLPAPER_EXT: ClassVar[str] = ".png"
    CUSTOM_INSTALL_SCRIPT_FILENAME: ClassVar[str] = "install.py"
    SETUPTOOLS_INSTALL_SCRIPT_FILENAME: ClassVar[str] = "setup.py"
    INTERNAL_PYTHON_COMMAND: ClassVar[str] = INTERNAL_PYTHON_COMMAND

    def make_essentials(self):
        """ Build a tuple of essential processes to run. """
        result = (
            {
                "imperative": "Check OS",
                "gerund": "Checking OS",
                "method": self.check_os
            }, {
                "imperative": "Update and upgrade",
                "gerund": "Updating and upgrading",
                "method": self.update_and_upgrade
            }, {
                "imperative": "Set up Git",
                "gerund": "Setting up Git",
                "method": self.set_up_git
            }
        )
        return result

    def make_non_essentials(self):
        """ Build a tuple of non-essential processes to run. """
        result = (
            {
                "imperative": "Install Google Chrome",
                "gerund": "Installing Google Chrome",
                "method": self.install_google_chrome
            }, {
                "imperative": "Install Kingdom of Cyprus",
                "gerund": "Installing Kingdom of Cyprus",
                "method": self.install_kingdom_of_cyprus
            }, {
                "imperative": "Install Chancery repos",
                "gerund": "Installing Chancery repos",
                "method": self.install_chancery
            }, {
                "imperative": "Install HGMJ",
                "gerund": "Installing HGMJ",
                "method": self.install_hgmj
            }, {
                "imperative": "Install SQLite",
                "gerund": "Installing SQLite",
                "method": self.install_sqlite
            }, {
                "imperative": "Install other third party",
                "gerund": "Installing other third party",
                "method": self.install_other_third_party
            }
        )
        return result

    def check_os(self):
        """ Test whether the OS we're using is supported. """
        if self.this_os in self.SUPPORTED_OSS:
            return True
        return False

    def set_up_git(self):
        """ Install Git and set up a personal access token. """
        install_result = self.install_via_apt("git")
        if not install_result:
            return False
        pat_result = \
            set_up_git_credentials(
                username=self.git_username,
                email_address=self.email_address,
                path_to_git_credentials=self.path_to_git_credentials,
                path_to_pat=self.path_to_pat
            )
        if not pat_result:
            return False
        return True

    def install_google_chrome(self):
        """ Ronseal. """
        if (
            check_command_exists("google-chrome") or
            (self.this_os == "chrome-os")
        ):
            return True
        chrome_url = urllib.parse.urljoin(self.CHROME_STEM, self.CHROME_DEB)
        chrome_deb_path = "./"+self.CHROME_DEB
        download_process = subprocess.run(["wget", chrome_url])
        if download_process.returncode != 0:
            return False
        if not self.install_via_apt(chrome_deb_path):
            return False
        os.remove(chrome_deb_path)
        return True

    def change_wallpaper(self):
        """ Change the wallpaper on the desktop of this computer. """
        if not Path(self.path_to_wallpaper_dir).exists():
            return False
        if self.thunderbird_num:
            wallpaper_filename = (
                self.WALLPAPER_STEM+
                str(self.thunderbird_num)+
                self.WALLPAPER_EXT
            )
        else:
            wallpaper_filename = "default.jpg"
        wallpaper_path = \
            str(Path(self.path_to_wallpaper_dir)/wallpaper_filename)
        if self.this_os == "ubuntu":
            arguments = [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                "picture-uri",
                "file:///"+wallpaper_path
            ]
        elif self.this_os == "raspbian":
            arguments = ["pcmanfm", "--set-wallpaper", wallpaper_path]
        else:
            return False
        result = self.run_with_indulgence(arguments)
        return result

    def make_git_url(self, repo_name):
        """ Make the URL pointing to a given repo. """
        suffix = self.git_username+"/"+repo_name+".git"
        result = urllib.parse.urljoin(self.GIT_URL_STEM, suffix)
        return result

    def install_own_repo(self, repo_name, installation_arguments=None):
        """ Install a custom repo. """
        if Path(repo_name).exists():
            print("Looks like "+repo_name+" already exists...")
            return True
        arguments = ["git", "clone", self.make_git_url(repo_name)]
        if not self.run_with_indulgence(arguments):
            return False
        with change_working_directory(repo_name):
            if installation_arguments:
                if not self.run_with_indulgence(arguments):
                    return False
            elif Path(self.CUSTOM_INSTALL_SCRIPT_FILENAME).exists():
                arguments = [
                    self.INTERNAL_PYTHON_COMMAND,
                    self.CUSTOM_INSTALL_SCRIPT_FILENAME
                ]
                if not self.run_with_indulgence(arguments):
                    return False
            elif Path(self.SETUPTOOLS_INSTALL_SCRIPT_FILENAME).exists():
                install_dependency(".")
            return True

    def install_kingdom_of_cyprus(self):
        """ Install the Kingdom of Cyprus repo. """
        return self.install_own_repo("kingdom-of-cyprus")

    def install_chancery(self):
        """ Install the Chancery repos. """
        if not self.install_own_repo("chancery"):
            return False
        if not self.install_own_repo("chancery-b"):
            return False
        return True

    def install_hgmj(self):
        """ Install the HGMJ repo. """
        return self.install_own_repo("hgmj")

    def install_other_third_party(self):
        """ Install some other useful packages. """
        result = True
        for package in self.OTHER_THIRD_PARTY:
            if not self.install_via_apt(package):
                result = False
        if self.this_os == "chrome-os":
            for package in self.MISSING_FROM_CHROME:
                if not self.install_via_apt(package):
                    result = False
        return result

    def get_sudo(self):
        """ Get superuser privileges. """
        if self.test_run:
            return
        print("I'm going to need superuser privileges for this...")
        subprocess.run(
            ["sudo", "echo", "Superuser privileges: activate!"],
            check=True
        )

    def run_with_indulgence(self, arguments):
        """ Run a command, and don't panic immediately if we get a non-zero
        return code. """
        if self.test_run:
            return True
        if self.show_output:
            print("Running subprocess.run() with arguments:")
            print(arguments)
            process = subprocess.run(arguments)
        else:
            process = subprocess.run(arguments, stdout=subprocess.DEVNULL)
        if process.returncode == 0:
            return True
        return False

    def run_apt_with_argument(self, argument):
        """ Run APT with an argument, and tell me how it went. """
        arguments = ["sudo", "apt-get", "--yes", argument]
        result = self.run_with_indulgence(arguments)
        return result

    def check_against_dpkg(self, package_name):
        """ Check whether a given package is on the books with DPKG. """
        result = self.run_with_indulgence(["dpkg", "--status", package_name])
        return result

    def install_via_apt(self, package_name, command=None):
        """ Attempt to install a package, and tell me how it went. """
        if not command:
            command = package_name
        if check_command_exists(command):
            return True
        arguments = ["sudo", "apt-get", "--yes", "install", package_name]
        result = self.run_with_indulgence(arguments)
        return result

    def update_and_upgrade(self):
        """ Update and upgrade the existing software. """
        self.run_apt_with_argument("update")
        if not self.run_apt_with_argument("upgrade"):
            return False
        if not self.install_via_apt("software-properties-common"):
            return False
        return True

    def install_sqlite(self):
        """ Install both SQLite and a browser for it. """
        if not self.install_via_apt("sqlite"):
            return False
        if not self.install_via_apt("sqlitebrowser"):
            return False
        return True

    def run_essentials(self):
        """ Run those processes which, if they fail, we will have to stop
        the entire program there. """
        for item in self.make_essentials():
            print(item["gerund"]+"...")
            method_to_run = item["method"]
            if not method_to_run():
                self.failure_log.append(item["imperative"])
                return False
        return True

    def run_non_essentials(self):
        """ Run the installation processes. """
        result = True
        for item in self.make_non_essentials():
            print(item["gerund"]+"...")
            method_to_run = item["method"]
            if not method_to_run():
                self.failure_log.append(item["imperative"])
                result = False 
        print("Changing wallpaper...")
        if not self.change_wallpaper():
            self.failure_log.append("Change wallpaper")
            # It doesn't matter too much if this fails.
        return result

    def print_outcome(self, passed, with_flying_colours):
        """ Print a list of what failed to the screen. """
        if passed and with_flying_colours:
            print("Installation PASSED with flying colours!")
        elif passed:
            print("Installation PASSED but with non-essential failures.")
        else:
            print("Installation FAILED.")
        if not (passed and with_flying_colours):
            print("\nThe following items failed:\n")
            for item in self.failure_log:
                print("    * "+item)
            print(" ")

    def run(self):
        """ Run the software installer. """
        print("Running His Majesty's Software Installer...")
        self.get_sudo()
        with change_working_directory(self.target_dir):
            if not self.run_essentials():
                print("\nFinished.\n\n")
                self.print_outcome(False, False)
                return False
            if self.minimal:
                self.print_outcome(True, True)
                return True
            with_flying_colours = self.run_non_essentials()
            print("\nComplete!\n")
            self.print_outcome(True, with_flying_colours)
            return True

####################
# HELPER FUNCTIONS #
####################

@contextlib.contextmanager
def change_working_directory(path):
    """ Changes working directory and returns to previous on exit. """
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)

def check_command_exists(command):
    """ Check whether a given command exists on this computer. """
    if shutil.which(command):
        return True
    return False

def create_default_hmss_config_file(path_to=DEFAULT_PATH_TO_HMSS_CONFIG_FILE):
    """ Create the default HMSS config file. """
    if Path(path_to).exists():
        return
    with open(path_to, "w") as config_file:
        json.dump(
            DEFAULT_HMSS_ARGUMENT_DICT, config_file, indent=CODE_INDENTATION
        )

def make_installer_obj(argument_dict):
    """ Ronseal. """
    result = HMSoftwareInstaller()
    for attribute_name in argument_dict.keys():
        attribute_value = argument_dict[attribute_name]
        setattr(result, attribute_name, attribute_value)
    return result

def install_hmss(path_to_config_file=DEFAULT_PATH_TO_HMSS_CONFIG_FILE):
    """ Make the installer object, and then run it. """
    if not Path(path_to_config_file).exists():
        print(
            "No config file found. I'm going to create one for you now at "+
            path_to_config_file
        )
        create_default_hmss_config_file(path_to=path_to_config_file)
        print("Please have a look at this file, and then run me again.")
        return
    with open(path_to_config_file, "r") as config_file:
        argument_dict = json.load(config_file)
    installer_obj = make_installer_obj(argument_dict)
    installer_obj.run()
