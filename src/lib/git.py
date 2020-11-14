"""
Module delegated to handling git logic
"""

# Native Modules
import logging
import re

from singletons.github import GithubSingleton
from singletons.setup import SetupSingleton
from utils.general import format_ansi_string, format_success_message
from utils.unicode import ForeGroundColor

# Custom Modules
from lib import ssh

SETUP = SetupSingleton.get_instance()
GITHUB = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


def public_key_exists_on_github() -> bool:
    """
    Check if current public key passed in exists on github
    """
    current_key = ssh.get_public_key()
    public_keys = GITHUB.get_public_keys().json()

    pattern = re.compile(re.escape(current_key))

    key_found = next(filter(
        lambda x: re.match(pattern, x['key']), public_keys), None)

    if key_found:
        LOGGER.info(format_ansi_string('Git SSH has already been configured on'
                                       ' Github', ForeGroundColor.LIGHT_GREEN))
    else:
        LOGGER.info(format_ansi_string('Git SSH is not configured on Github',
                                       ForeGroundColor.LIGHT_RED))

    return key_found is not None


def upload_ssh_key_to_github():
    """
    Uploads the current SSH key to Github
    """
    current_public_key = ssh.get_public_key()

    payload = {
        'title': 'script-env-pub-key',
        'key': current_public_key
    }

    GITHUB.create_public_key(payload)


def delete_github_pub_key(current_key: str, public_keys: list):
    """
    Removes current public key in host machine stored on github
    """
    pattern = re.compile(re.escape(current_key))

    for key in public_keys:
        if re.match(pattern, key['key']):
            GITHUB.delete_public_key(key['id'])
            LOGGER.info(format_ansi_string('Provided public key now deleted '
                                           'from github account',
                                           ForeGroundColor.GREEN))
            return
    LOGGER.warning(format_ansi_string('Provided public key does not exist on '
                                      'GitHub or incorrect arguments',
                                      ForeGroundColor.YELLOW))


def remove_ssh_config():
    """
    Removes the identity value of the rsa private key from the ssh config file
    """
    ssh_config_file = f'{SETUP.directories.ssh}/config'

    with open(ssh_config_file) as text_file:
        content = ''.join(text_file.readlines())

    pattern = re.compile(r'IdentityFile .*')
    key_match = re.search(pattern, content)

    if not key_match:
        LOGGER.info(format_ansi_string('IdentityFile key value already '
                                       'deleted from ssh config file',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    start, end = key_match.span()

    content = content[:start] + content[end:]
    with open(ssh_config_file, 'w') as text_file:
        text_file.write(content)

    LOGGER.info(format_ansi_string('IdentityFile key value is now removed from'
                                   ' ssh config file', ForeGroundColor.GREEN))


def remove_ssh_github_host():
    """
    Remove host key & agent from known_host file in .ssh directory
    """
    known_hosts = f'{SETUP.directories.ssh}/known_hosts'

    with open(known_hosts) as text_file:
        content = ''.join(text_file.readlines())

    pattern = re.compile(r'github.* ssh-rsa .*')
    key_match = re.search(pattern, content)

    if not key_match:
        LOGGER.info(format_success_message(
            'Github host value already deleted from known_host file'))
        return

    start, end = key_match.span()

    content = content[:start] + content[end:]
    with open(known_hosts, 'w') as text_file:
        text_file.write(content)

    LOGGER.info(format_success_message(
        'Github host value is now removed from known_host file'))
