"""
Module delegated to handling git logic
"""

# Native Modules
import logging
import re

# Custom Modules
from services import ssh
from singletons.setup import SetupSingleton
from singletons.github import GithubSingleton
from utils.general import format_ansi_string
from utils.unicode import *

SETUP: SetupSingleton = SetupSingleton.get_instance()
GITHUB: GithubSingleton = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


def update_ssh_config():
    """
    Update config file in .ssh directory
    """
    ssh_config_file = f'{SETUP.ssh_dir}/config'

    with open(ssh_config_file) as text_file:
        content = ''.join(text_file.readlines())

    pattern = re.compile(r'IdentityFile .*')
    key_match = re.search(pattern, content)

    identity_val = f'IdentityFile {SETUP.home_dir}/.ssh/id_rsa'

    if not key_match:
        with open(ssh_config_file, 'a') as text_file:
            text_file.write(identity_val)
        LOGGER.info(format_ansi_string('IdentityFile key value appended to ssh '
                                       'config file', ForeGroundColor.GREEN))
        return

    start, end = key_match.span()
    current_config = content[start: end]

    if current_config == identity_val:
        LOGGER.info(format_ansi_string('IdentityFile key value already '
                                       'configured in ssh config file',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    content = content[:start] + identity_val + content[end:]
    with open(ssh_config_file, 'w') as text_file:
        text_file.write(content)

    LOGGER.info(format_ansi_string('IdentityFile key value updated in ssh '
                                   'config file', ForeGroundColor.GREEN))


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
        LOGGER.info(format_ansi_string('Git SSH has been configured on '
                                       'Github', ForeGroundColor.LIGHT_GREEN))
    else:
        LOGGER.info(format_ansi_string('Git SSH is not configured on Github',
                                       ForeGroundColor.LIGHT_RED))

    return key_found is not None


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
    ssh_config_file = f'{SETUP.ssh_dir}/config'

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

    LOGGER.info(format_ansi_string('IdentityFile key value is now removed from '
                                   'ssh config file', ForeGroundColor.GREEN))


def remove_ssh_github_host():
    """
    Remove host key & agent from known_host file in .ssh directory
    """
    known_hosts = f'{SETUP.ssh_dir}/known_hosts'

    with open(known_hosts) as text_file:
        content = ''.join(text_file.readlines())

    pattern = re.compile(r'github.* ssh-rsa .*')
    key_match = re.search(pattern, content)

    if not key_match:
        LOGGER.info(format_ansi_string('Github host value already deleted from '
                                       'known_host file',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    start, end = key_match.span()

    content = content[:start] + content[end:]
    with open(known_hosts, 'w') as text_file:
        text_file.write(content)

    LOGGER.info(format_ansi_string('Github host value is now removed from '
                                   'known_host file', ForeGroundColor.GREEN))
