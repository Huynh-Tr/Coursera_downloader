"""
Manages the credential information (passwords, etc).
"""

import getpass
import os


class CredentialsError(BaseException):
    """
    Class to be thrown if the credentials are not found.
    """

    pass


def _getenv_or_empty(s):
    """
    Helper function that converts None gotten from the environment to the
    empty string.
    """
    return os.getenv(s) or ""


def get_credentials(username=None, password=None):
    """
    Return valid username, password tuple.

    Raises CredentialsError if username or password is missing.
    """

    if not username:
        raise CredentialsError(
            "Please provide a username with the -u option, "
            "or a CAUTH cookie with the --cauth option"
        )

    if not password:
        password = getpass.getpass(f"Coursera password for {username}: ")

    return username, password
