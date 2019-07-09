'''
Wrapper object for setup script
'''

## System/Third-Party modules
import logging
import pprint
import sys
import requests

LOGGER = logging.getLogger()

class GithubWrapper():
    '''
    Wrapper object to handle GitHub API http request/responses only
    '''

    def __init__(self):
        git = read_git_credentials()

        self.api = 'https://api.github.com'
        self.username = git['username']
        self.email = git['email']
        self.token = git['token']

        self.common_headers = {}
        self.common_headers['Authorization'] = f'token {self.token}'

    def __str__(self):
        str_vals = {}
        str_vals['api_url'] = self.api
        str_vals['username'] = self.username
        str_vals['email'] = self.email
        str_vals['token'] = self.token
        str_vals['common_headers'] = self.common_headers
        pretty_str = pprint.pformat(str_vals)
        return pretty_str

    def get_public_keys(self) -> dict:
        '''
        Retrieve list of existing public keys for configured user
        '''
        url = f'{self.api}/users/{self.username}/keys'

        try:
            res = requests.get(url, timeout=3)
            res.raise_for_status()
        except requests.RequestException as req_err:
            LOGGER.error(f'Request Error occurred: {req_err}')
            LOGGER.error(f'Returned response: {res.json()}')
            LOGGER.error('Failed request to GitHub API to get public keys')
            sys.exit()
        else:
            return res

    def create_public_key(self, payload: dict):
        '''
        Create public key given input to github user account
        '''
        url = f'{self.api}/user/keys'

        try:
            res = requests.post(url, json=payload, headers=self.common_headers, timeout=3)
            res.raise_for_status()
        except requests.RequestException as req_err:
            LOGGER.error(f'Request Error occurred: {req_err}')
            LOGGER.error(f'Returned response: {res.json()}')
            LOGGER.error('Failed request to GitHub API to create a public key')
            sys.exit()
        else:
            return res

    def delete_public_key(self, key_id: int):
        '''
        Delete given public key from github user account
        '''
        url = f'{self.api}/user/keys/{key_id}'

        try:
            res = requests.delete(url, headers=self.common_headers, timeout=3)
            res.raise_for_status()
        except requests.RequestException as req_err:
            LOGGER.error(f'Request Error occurred: {req_err}')
            LOGGER.error(f'Returned response: {res.json()}')
            LOGGER.error('Failed request to GitHub API to delete a public key')
            sys.exit()
        else:
            return res

def read_git_credentials() -> dict:
    '''
    Read credentials from file into wrapper object from project directory
    '''
    res = {}
    git_credentials = 'config/git-credentials.txt'
    valid_properties = ['username', 'email', 'token']

    buff = None
    try:
        with open(git_credentials) as text_file:
            buff = [line for line in text_file.readlines()]
    except IOError as ierr:
        # Generate git credential template
        with open(git_credentials, 'w') as text_file:
            for prop in valid_properties:
                text_file.write(f'{prop}: <INSERT OWN VALUE>\n')

        LOGGER.error(ierr)
        LOGGER.error(f'Git credential file does not exist - now generated in {git_credentials}')
        sys.exit()

    for line in buff:
        key, val = line.split(':')
        key, val = key.strip(), val.strip()

        if not key or not val:
            LOGGER.error('Git credentials are not configured properly')
            sys.exit()
        if key not in valid_properties:
            LOGGER.error('Git property is invalid')
            sys.exit()
        if val[0] == '<' or val[-1] == '>':
            LOGGER.error('Git value of property is unset or invalid')
            sys.exit()

        res[key] = val
    return res

GITHUB = GithubWrapper()
