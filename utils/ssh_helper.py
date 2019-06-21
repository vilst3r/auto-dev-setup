'''
Module delegated to handling ssh logic
'''

# System/Third-Party modules
from subprocess import call, Popen, check_output, PIPE, DEVNULL

# Custom modules
from utils.setup_wrapper import SetupWrapper
from utils.github_wrapper import GithubWrapper

SETUP = SetupWrapper()
GITHUB = GithubWrapper()

def ssh_public_key_exists() -> bool:
    '''
    Check if public key exists to confirm whether ssh is already configured
    '''
    home_dir = SETUP.dir['home']

    command = f'find {home_dir}/.ssh/id_rsa.pub'
    file_found = call(command.split(), stdout=DEVNULL, stderr=DEVNULL)

    return file_found == 0

def generate_rsa_ssh_keypair():
    '''
    Generate asymmetric public/private keypair for ssh use
    '''
    git_email = GITHUB.email

    command = f'ssh-keygen -t rsa -b 4096 -C \"{git_email}\" -N foobar'

    with Popen(command.split(), stdin=PIPE) as process:
        process.communicate(input=b'\ny\n')

def start_ssh_agent():
    '''
    Start ssh-agent process in local machine
    '''
    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'eval \"$(ssh-agent -s)\"')
    call(command_list)

def register_private_key_to_ssh_agent():
    '''
    Add ssh private key to ssh-agent
    '''
    home_dir = SETUP.dir['home']

    command = f'ssh-add -K {home_dir}/.ssh/id_rsa'
    call(command.split())

def get_ssh_public_key() -> str:
    '''
    Return utf-8 string of ssh public key
    '''
    home_dir = SETUP.dir['home']

    command = f'cat {home_dir}/.ssh/id_rsa.pub'
    output = check_output(command.split())
    parsed_output = output.decode('utf-8').split()
    key_type = parsed_output[0]
    key_data = parsed_output[1]

    public_key = f'{key_type} {key_data}'
    return public_key
