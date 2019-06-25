#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

'''
Process outline (rollback flow from setup)
1. Pip uninstall powerline-gitstatus
2. Remove the git cloned font folder in the config folder
3. Delete user config of powerline in '~/.config/powerline'
4. Remove powerline config block in bash_profile
5. Remove the powerline config block in vimrc
6. Pip uninstall powerline-status
7. Remove the git cloned bash-settings folder in the config folder
8. Delete all the color themes in '~/.vim.colors'
9. Remove the git cloned vim-settings folder in the config folder
10. Uninstall homebrew to uninstall all the cask & brew packages
11. Delete public key from GitHub
12. Delete local ssh public key and private key
13. Stop ssh agent
14. Remove git host key from the ssh config file
15. Remove the host agent from config file
16. All done
'''

# System/Third-Party modules
import subprocess
from subprocess import PIPE, DEVNULL
import time
import re

# Custom modules
from utils.setup_wrapper import SetupWrapper
from utils.github_wrapper import GithubWrapper
import utils.powerline_helper as powerline_helper
import utils.git_helper as git_helper


def remove_powerline():
    '''
    Remove existing powerline configurations
    '''
    home_dir = SETUP.dir['home']
    python_site = SETUP.dir['python_site']
    powerline_config = SETUP.dir['powerline_config']

    # blah

if __name__ == '__main__':
#    remove_powerline()
#    configure_git_ssh()
#    install_homebrew()
#    install_brew_packages()
#    install_cask_packages()
#    configure_vim()
#    configure_bash()
#    install_powerline()

