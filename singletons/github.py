"""
Singleton object for setup script
"""

## Native Modules
import logging
import pprint
import sys

# Custom Modules
from utils.general import format_ansi_string
from utils.unicode import *


# Third Party Modules
import requests

LOGGER = logging.getLogger()


class GithubSingleton:
    """
    Singleton object to handle GitHub API http request/responses only
    """

    __instance = None

    def _initialize_singleton(self):
        """ Initialise the singleton"""
        git = read_git_credentials()

        self.api = 'https://api.github.com'
        self.username = git['username']
        self.email = git['email']
        self.token = git['token']

        self.common_headers = {}
        self.common_headers['Authorization'] = f'token {self.token}'

    def __init__(self):
        """ Virtually private constructor """
        if GithubSingleton.__instance:
            raise Exception('Class already instantiated')

        self._initialize_singleton()
        GithubSingleton.__instance = self

        LOGGER.debug(f'GithubSingleton:\n {self}')

    def __str__(self):
        return pprint.pformat(self.__dict__)

    def get_public_keys(self) -> dict:
        """
        Retrieve list of existing public keys for configured user
        """
        url = f'{self.api}/users/{self.username}/keys'

        try:
            res = requests.get(url, timeout=3)
            res.raise_for_status()
        except requests.RequestException as req_err:
            LOGGER.error(f'Request Error occurred: {req_err}')
            LOGGER.error(f'Returned response: {res.json()}')
            LOGGER.error(format_ansi_string('Failed request to GitHub API to '
                                            'get public keys',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            return res

    def create_public_key(self, payload: dict):
        """
        Create public key given input to github user account
        """
        url = f'{self.api}/user/keys'

        try:
            res = requests.post(
                url, json=payload, headers=self.common_headers, timeout=3
            )
            res.raise_for_status()
        except requests.RequestException as req_err:
            LOGGER.error(f'Request Error occurred: {req_err}')
            LOGGER.error(f'Returned response: {res.json()}')
            LOGGER.error(format_ansi_string('Failed request to GitHub API to '
                                            'create a public key',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.info(format_ansi_string('Github public key has '
                                           'successfully been created!',
                                           ForeGroundColor.GREEN))
            return res

    def delete_public_key(self, key_id: int):
        """
        Delete given public key from github user account
        """
        url = f'{self.api}/user/keys/{key_id}'

        try:
            res = requests.delete(url, headers=self.common_headers, timeout=3)
            res.raise_for_status()
        except requests.RequestException as req_err:
            LOGGER.error(f'Request Error occurred: {req_err}')
            LOGGER.error(f'Returned response: {res.json()}')
            LOGGER.error(format_ansi_string('Failed request to GitHub API to '
                                            'delete a public key',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            return res

    @staticmethod
    def get_instance():
        """ Static access method """
        if not GithubSingleton.__instance:
            GithubSingleton()
        return GithubSingleton.__instance


def read_git_credentials() -> dict:
    """
    Read credentials from file into wrapper object from project directory
    TODO - think about refactoring this later...
    """
    res = {}
    git_credentials = 'config/git-credentials.txt'
    valid_properties = ['username', 'email', 'token']

    try:
        with open(git_credentials) as text_file:
            buff = text_file.readlines()
    except IOError as ierr:
        # Generate git credential template
        with open(git_credentials, 'w') as text_file:
            for prop in valid_properties:
                text_file.write(f"{prop}: <INSERT OWN VALUE>\n")

        LOGGER.error(ierr)
        LOGGER.error(format_ansi_string(f'Git credential file does not exist '
                                        f'- now generated in {git_credentials}',
                                        ForeGroundColor.RED))
        sys.exit()

    for line in buff:
        key, val = line.split(':')
        key, val = key.strip(), val.strip()

        if not key or not val:
            LOGGER.error(format_ansi_string('Git credentials are not '
                                            'configured properly',
                                            ForeGroundColor.RED))
            sys.exit()
        if key not in valid_properties:
            LOGGER.error(format_ansi_string('Git property is invalid',
                                            ForeGroundColor.RED))
            sys.exit()
        if val[0] == '<' or val[-1] == '>':
            LOGGER.error(format_ansi_string('Git value of property is unset '
                                            'or invalid', ForeGroundColor.RED))
            sys.exit()

        res[key] = val
    return res
