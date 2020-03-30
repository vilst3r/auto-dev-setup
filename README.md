# auto-dev-setup

Python script to replicate personal development environment across any machine 
with proper packaging, editor profiles & settings. OSX machine environment only.

# Requirements
- Python3 to run the script
- Latest version of pip3 otherwise the script requires a second run to complete
    - Run `pip3 install -r requirements` to fetch all script dependencies
         after installing pip3

# Automated Process
1. Configure git ssh key
2. Installs homebrew 
3. Installs brew packages from './config/brew/brew.txt'
4. Installs brew cask software from './config/brew/brew-cask.txt'
5. Install & Configure vim
6. Install & Configure bash
7. Install & Configure powerline

# Notes
- Password is required when OS X prompts you to enter your password for the 
    keychain access, choosing 'Always Allow' would make the whole process 
    seamless without any prompts from then onwards
- iTerm2 configuration left to manual user configuration through the GUI

# TODO
- Add iTerm2 configuration in spare time in the future
