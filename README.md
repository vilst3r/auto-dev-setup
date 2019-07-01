# env-setup

Python scripts to replicate personal development environment across any machine with proper packaging and editor profiles and settings. Linux machine environment only.

# Requirements
- Python 3 system binary installed to run the script
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
- Configure iterm2 font to configure last step of powerline
- iTerm2 configuration left to manual user intervention
