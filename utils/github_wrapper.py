'''
Wrapper object for setup script
'''

## System/Third-Party modules
import requests

class GithubWrapper():
    '''
    Wrapper object to handle GitHub API http request/responses only
    '''

    def __init__(self, git: dict):
        self.api = 'https://api.github.com'

        valid_properties = ['username', 'email', 'token']
        if not all([key in valid_properties for key in git]):
            raise Exception('Git object passed in GithubWrapper isn\'t valid')

        self.username = git['username']
        self.email = git['email']
        self.token = git['token']

        self.common_headers = {}
        self.common_headers['Authorization'] = f'token {self.token}'

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
