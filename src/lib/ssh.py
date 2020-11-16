"""
Module delegated to handling ssh logic
"""

import logging
import re
# Native Modules
import sys
from subprocess import DEVNULL, PIPE, Popen, call

from singletons.github import GithubSingleton
# Custom Modules
from singletons.setup import SetupSingleton
from utils.general import consume, format_ansi_string
from utils.unicode import ForeGroundColor

SETUP = SetupSingleton.get_instance()
GITHUB = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


def public_key_exists() -> bool:
    """
    Check if public key exists to confirm whether ssh is already configured
    """
    command = f'find {SETUP.directories.ssh}/id_rsa.pub'
    file_found = call(command.split(), stdout=DEVNULL, stderr=DEVNULL) == 0

    if not file_found:
        LOGGER.info(format_ansi_string('Git SSH hasn\'t been configured '
                                       'locally', ForeGroundColor.LIGHT_RED))
    else:
        LOGGER.info(format_ansi_string('Git SSH has already been configured '
                                       'locally', ForeGroundColor.LIGHT_GREEN))

    return file_found


def generate_rsa_keypair():
    """
    Generate asymmetric public/private keypair for ssh use
    """
    command = f'ssh-keygen -t rsa -b 4096 -C \"{GITHUB.email}\" -N\
                {SETUP.ssh_passphrase}'
    with Popen(command.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE) \
            as process:
        out, err = process.communicate(input=b'\ny\n')

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('RSA keypair for SSH failed to '
                                            'generated', ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('RSA keypair for SSH has '
                                           'successfully been generated',
                                           ForeGroundColor.GREEN))


def start_ssh_agent():
    """
    Start ssh-agent process in local machine
    """
    def find_ssh_process(line):
        """
        Processes output to log the ssh agent process
        """
        if not line:
            return

        user, pid = line.split()[:2]

        if 'egrep' not in line and user == SETUP.username:
            LOGGER.debug(f'Existing ssh-agent pid - {pid}')
            LOGGER.debug(f'{line}')

    command = 'ps aux'
    ps_process = Popen(command.split(), stdout=PIPE)

    command = 'egrep ssh-agent'
    with Popen(command.split(), stdin=ps_process.stdout, stdout=PIPE) \
            as process:
        out, err = process.communicate()
        grepped = process.returncode == 0
        ps_process.communicate()

        if err and not grepped:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to grep for the ssh-agent'
                                            ' process', ForeGroundColor.RED))
            sys.exit()

        parsed_output = out.decode('utf-8').split('\n')

    consume(map(lambda x: find_ssh_process(x), parsed_output))

    command_list = ['sh', '-c', f'eval \"$(ssh-agent -s)\"']
    with Popen(command_list, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('SSH-agent process failed to '
                                            'start', ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('SSH-agent process has '
                                           'successfully started',
                                           ForeGroundColor.GREEN))


def update_config_identity():
    """
    Update config file in .ssh directory
    """
    ssh_config_file = f'{SETUP.directories.ssh}/config'

    command = f'touch {ssh_config_file}'
    call(command.split(), stdout=DEVNULL)

    with open(ssh_config_file) as text_file:
        content = ''.join(text_file.readlines())

    pattern = re.compile(r'IdentityFile .*')
    key_match = re.search(pattern, content)

    identity_val = f'IdentityFile {SETUP.directories.ssh}/id_rsa'

    if not key_match:
        with open(ssh_config_file, 'a') as text_file:
            text_file.write("Host *\n")
            text_file.write("AddKeysToAgent yes\n")
            text_file.write("UseKeychain yes\n")
            text_file.write(identity_val)
        LOGGER.info(format_ansi_string('IdentityFile key value appended to ssh'
                                       ' config file', ForeGroundColor.GREEN))
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


def register_private_key_to_ssh_agent():
    """
    Add ssh private key to ssh-agent
    """
    LOGGER.info(format_ansi_string(f'Passphrase for the newly generated SSH key '
                                   f'to cache - {SETUP.ssh_passphrase}'))

    command = f'ssh-add -K {SETUP.directories.ssh}/id_rsa'
    ssh_added = call(command.split(), stdout=DEVNULL) == 0

    if ssh_added:
        LOGGER.info(format_ansi_string('SSH private key has successfully been'
                                       ' added to the ssh-agent',
                                       ForeGroundColor.GREEN))
    else:
        LOGGER.error(format_ansi_string('SSH private key coudln\'t be added '
                                        'to the ssh-agent',
                                        ForeGroundColor.RED))
        sys.exit()


def get_public_key() -> str:
    """
    Return utf-8 string of ssh public key
    """
    command = f'cat {SETUP.directories.ssh}/id_rsa.pub'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('SSH public key is missing',
                                            ForeGroundColor.RED))
            sys.exit()

        LOGGER.debug(out.decode('utf-8'))
        parsed_output = out.decode('utf-8').split()
        key_type = parsed_output[0]
        key_data = parsed_output[1]

        public_key = f'{key_type} {key_data}'
        return public_key


def delete_ssh_rsa_keypair():
    """
    Delete both public and private key configured for ssh
    """
    command_list = ['sh', '-c', f'rm {SETUP.directories.ssh}/id_rsa*']

    with Popen(command_list, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to remove RSA keypairs '
                                            'configured for SSH',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('RSA keypairs configured for SSH '
                                           'has successfully been removed',
                                           ForeGroundColor.GREEN))


def stop_ssh_agent():
    """
    Stop process responsible for ssh connections
    TODO - refactor logic to functional later...
    """
    command = 'ps aux'
    ps_process = Popen(command.split(), stdout=PIPE)

    command = 'egrep ssh-agent'
    egrep_process = Popen(
        command.split(), stdin=ps_process.stdout, stdout=PIPE)

    out, err = egrep_process.communicate()
    grepped = egrep_process.returncode == 0

    if err and not grepped:
        LOGGER.error(err.decode('utf-8'))
        LOGGER.error(format_ansi_string('Failed to grep', ForeGroundColor.RED))
        sys.exit()

    ps_process.communicate()

    pids_to_kill = []
    parsed_output = out.decode('utf-8').split('\n')
    for line in parsed_output:
        if not line:
            continue

        user, pid = line.split()[:2]

        if 'egrep' not in line and user == SETUP.username:
            LOGGER.debug(f'Existing ssh-agent pid - {pid}')
            LOGGER.debug(f'{line}')
            pids_to_kill.append(pid)

    for pid in pids_to_kill:
        command = f'kill {pid}'
        with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
            out, err = process.communicate()

            if err:
                LOGGER.error(err.decode('utf-8'))
                LOGGER.error(format_ansi_string('Failed to stop ssh-agent '
                                                'process',
                                                ForeGroundColor.RED))
                sys.exit()
            else:
                LOGGER.debug(out.decode('utf-8'))
                LOGGER.debug('SSH-agent pid {pid} has been terminated')

    LOGGER.info(format_ansi_string('SSH-agent process has successfully been '
                                   'stopped', ForeGroundColor.GREEN))
