#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

'''
Process outline (rollback flow from setup)
1. Pip uninstall powerline-gitstatus(done)
2. Remove the git cloned font folder in the config folder(done)
3. Delete user config of powerline in '~/.config/powerline'(done)
4. Remove powerline config block in bash_profile(done)
5. Remove the powerline config block in vimrc(done)
6. Pip uninstall powerline-status(done)
7. Remove the git cloned bash-settings folder in the config folder(done)
8. Delete all the color themes in '~/.vim.colors' (done)
9. Remove the git cloned vim-settings folder in the config folder(done)
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
from utils.setup_wrapper import SETUP
from utils.github_wrapper import GITHUB
import utils.powerline_helper as powerline_helper
import utils.git_helper as git_helper
import utils.ssh_helper as ssh_helper
import utils.brew_helper as brew_helper
import utils.vim_helper as vim_helper
import utils.bash_helper as bash_helper

def uninstall_powerline():
    '''
    Remove existing powerline configurations
    '''
    powerline_helper.uninstall_gitstatus()
    powerline_helper.delete_fonts()
    powerline_helper.delete_config()
    powerline_helper.remove_bash_daemon()
    powerline_helper.remove_vim_config()
    powerline_helper.uninstall_powerline()

def pretty_print_wrapper(wrapper: object, title: str):
    '''
    Function to pretty print wrapper in beginning of cleanup
    '''
    print(f'###### {title} #####')
    print(f'\n{wrapper}\n')


if __name__ == '__main__':
    START = time.time()
    pretty_print_wrapper(SETUP, 'SetupWrapper')
    pretty_print_wrapper(GITHUB, 'GithubWrapper')

    uninstall_powerline()
#    configure_git_ssh()
#    install_homebrew()
#    install_brew_packages()
#    install_cask_packages()
#    configure_vim()
#    configure_bash()
#    install_powerline()
    END = time.time()
    print(f'\nSetup time: {END - START} seconds\n')
