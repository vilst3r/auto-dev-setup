'''
Wrapper object for setup script
'''

## System/Third-Party modules
import requests
import pprint

# Custom modules
from utils.io_helper import *

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
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
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
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
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
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return res

def read_git_credentials() -> dict:
    '''
    Read credentials from file into wrapper object from project directory
    '''
    res = {}
    valid_properties = ['username', 'email', 'token']

    buff = read_file('config/git-credentials.txt')
    for line in buff:
        key, val = line.split(':')

        if not key or not val:
            raise Exception('Git credentials are not configured properly')
        if key not in valid_properties:
            raise Exception('Git property is invalid')

        key, val = key.strip(), val.strip()
        res[key] = val
    return res
