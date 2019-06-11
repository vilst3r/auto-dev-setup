'''
Wrapper object for setup script
'''

## System/Third-Party modules
import requests

## Custom modules

class GithubWrapper():
    '''
    Wrapper object to handle GitHub API http resuest/responses only
    '''

    def __init__(self, git: dict):
        self.api = 'https://api.github.com'

        self.verify_config(git)
        self.username = git['username']
        self.email = git['email']
        self.token = git['token']

    def verify_config(self, git: dict):
        '''
        Verify git credential file keys
        '''
        valid_keys = ['username', 'email', 'token']
        return all(key in valid_keys for key in git)

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
            return res.json()

    def create_public_key(self, payload: dict):
        '''
        Create public key given input to github user account
        '''
        url = f'{self.api}/user/keys'
        headers = {}
        headers['Authorization'] = f'token {self.token}'

        try:
            res = requests.post(url, json=payload, headers=headers, timeout=3)
            res.raise_for_status()
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(res.json())
        except Exception as err:
            print(f'Other error occurred: {err}')
            print(res.json())
        else:
            return res.json()

    def delete_public_key(self, key_id: int):
        '''
        Delete given public key from github user account
        '''
        url = f'{self.api}/user/keys/{key_id}'
        headers = {}
        headers['Authorization'] = f'token {self.token}'

        try:
            res = requests.delete(url, headers=headers)
            res.raise_for_status()
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(res.json())
        except Exception as err:
            print(f'Other error occurred: {err}')
            print(res.json())
        else:
            return res
