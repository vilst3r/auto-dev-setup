# env-setup

Python scripts to replicate personal development environment across any machine with proper packaging and editor profiles and settings. Linux machine environment only.

# Requirements
- Python3 to run the script
- Latest version of pip3 otherwise the script requires a second run to complete
- Run `pip3 install -r requirements` to fetch all script dependencies

# Automated Process
1. Configure git ssh key (requires passcode)
2. Installs homebrew (requires passcode)
3. Installs brew packages from './config/brew/brew.txt'
4. Installs brew cask software from './config/brew/brew-cask.txt'
5. Install & Configure vim
6. Install & Configure bash
7. Install & Configure powerline

# Notes
- iTerm2 configuration left to manual user configuration through the GUI
- Add script to restart powerline-daemon
    - `powerline-daemon -r`
