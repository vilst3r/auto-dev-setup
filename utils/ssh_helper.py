'''
Module delegated to handling ssh logic
'''

# System/Third-Party modules
import sys
import logging
from subprocess import call, Popen, PIPE, DEVNULL

# Custom modules
from utils.setup_wrapper import SETUP
from utils.github_wrapper import GITHUB

LOGGER = logging.getLogger()

def public_key_exists() -> bool:
    '''
    Check if public key exists to confirm whether ssh is already configured
    '''
    home_dir = SETUP.dir['home']

    command = f'find {home_dir}/.ssh/id_rsa.pub'
    file_found = call(command.split(), stdout=DEVNULL, stderr=DEVNULL) == 0

    if not file_found:
        LOGGER.info('Git SSH hasn\'t been configured locally - configuring now...')
    else:
        LOGGER.info('Git SSH has been configured locally')

    return file_found

def generate_rsa_keypair():
    '''
    Generate asymmetric public/private keypair for ssh use
    '''
    command = f'ssh-keygen -t rsa -b 4096 -C \"{GITHUB.email}\" -N foobar'

    with Popen(command.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate(input=b'\ny\n')

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('RSA keypair for SSH has failed to generated')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('RSA keypair for SSH has successfully been generated')

def start_ssh_agent():
    '''
    Start ssh-agent process in local machine
    '''
    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'eval \"$(ssh-agent -s)\"')

    with Popen(command_list, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('SSH-agent process has failed to start')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('SSH-agent process has successfully started')

def register_private_key_to_ssh_agent():
    '''
    Add ssh private key to ssh-agent
    '''
    home_dir = SETUP.dir['home']

    command = f'ssh-add -K {home_dir}/.ssh/id_rsa'
    ssh_added = call(command.split(), stdout=DEVNULL) == 0

    if ssh_added:
        LOGGER.info('SSH private key has successfully been added to the ssh-agent')
    else:
        LOGGER.error('SSH private key has failed to be added to the ssh-agent')
        sys.exit()

def get_public_key() -> str:
    '''
    Return utf-8 string of ssh public key
    '''
    home_dir = SETUP.dir['home']

    command = f'cat {home_dir}/.ssh/id_rsa.pub'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('SSH public key is missing')
            sys.exit()

        LOGGER.debug(out.decode('utf-8'))
        parsed_output = out.decode('utf-8').split()
        key_type = parsed_output[0]
        key_data = parsed_output[1]

        public_key = f'{key_type} {key_data}'
        return public_key

def delete_ssh_rsa_keypair():
    '''
    Delete both public and private key configured for ssh
    '''
    home_dir = SETUP.dir['home']

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'rm {home_dir}/.ssh/id_rsa*')

    with Popen(command_list, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to remove RSA keypairs configured for SSH')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('RSA keypairs configured for SSH has successfully been removed')

def stop_ssh_agent():
    '''
    Stop process responsible for ssh connections
    '''
    command = 'ps aux'
    ps_process = Popen(command.split(), stdout=PIPE)

    command = 'egrep /usr/bin/ssh-agent'
    egrep_process = Popen(command.split(), stdin=ps_process.stdout, stdout=PIPE)

    out = egrep_process.communicate()[0]
    ps_process.communicate()

    pid = out.decode('utf-8').split()[1]

    command = f'kill {pid}'

    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to stop ssh-agent process')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('SSH-agent process has successfully been stopped')
