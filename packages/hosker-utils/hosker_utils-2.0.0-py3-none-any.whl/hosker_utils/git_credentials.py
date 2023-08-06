"""
This code sets up the Git credentials for this computer.
"""

# Standard imports.
import subprocess
from pathlib import Path

# Local imports.
from .hmss_config import (
    DEFAULT_EMAIL_ADDRESS,
    DEFAULT_ENCODING,
    DEFAULT_GIT_USERNAME,
    DEFAULT_PATH_TO_GIT_CREDENTIALS,
    DEFAULT_PATH_TO_PAT
)

#############
# FUNCTIONS #
#############

def make_github_credential(pat, username=DEFAULT_GIT_USERNAME):
    """ Generate a string for a GitHub credential, given a username and a
    personal access token. """
    result = "https://"+username+":"+pat+"@github.com"
    return result

def set_username_and_email_address(
        username=DEFAULT_GIT_USERNAME,
        email_address=DEFAULT_EMAIL_ADDRESS
    ):
    """ Set the global Git ID configurations for this device. """
    subprocess.run(
        ["git", "config", "--global", "user.name", username],
        check=True
    )
    subprocess.run(
        ["git", "config", "--global", "user.email", email_address],
        check=True
    )

def set_up_git_credentials(
        username=DEFAULT_GIT_USERNAME,
        email_address=DEFAULT_EMAIL_ADDRESS,
        path_to_git_credentials=DEFAULT_PATH_TO_GIT_CREDENTIALS,
        path_to_pat=DEFAULT_PATH_TO_PAT,
        encoding=DEFAULT_ENCODING
    ):
    """ Set up GIT credentials, if necessary and possible. """
    path_to = path_to_git_credentials # A useful abbreviation.
    set_username_and_email_address(
        username=username,
        email_address=email_address
    )
    if Path(path_to_pat).exists():
        with open(path_to_pat, "r", encoding=encoding) as pat_file:
            pat = pat_file.read()
            while pat.endswith("\n"):
                pat = pat[:-1]
        credential = make_github_credential(pat)
        with open(path_to, "w", encoding=encoding) as credentials_file:
            credentials_file.write(credential)
    elif not Path(path_to).exists():
        print(
            "Error setting up GIT credentials: could not find PAT at "+
            path_to_pat+" or GIT credentials at "+path_to
        )
        return False
    config_string = "store --file "+path_to
    subprocess.run(
        ["git", "config", "--global", "credential.helper", config_string],
        check=True
    )
    print("GIT credentials set up!")
    return True
