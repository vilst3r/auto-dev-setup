# env-setup

Python scripts to replicate personal development environment across any machine with proper packaging and editor profiles and settings. Linux machine environment only.

# Process
1. Installs homebrew
2. Installs brew packages from './config/brew.txt'
3. Installs brew cask software from './config/brew-cask.txt'
4. Configures vim & bash from project directory
5. Configure git ssh key
6. Install powerline
...

# Todo
- Remove vim scripts locally and just pull from git to remove percentage of my vim script lol
- Fucked up my project name in regards to package importing, might need to change it all
- Move helper functions into a seperate module
- Make API call to GitHub to add SSH Key for local machine
- Consolidate the powerline configurations with the fonts and styling applied
- Configure styling of vim gruvbox theme into setup
- Configure iterm2 profile somehow...
- Modify forks to be compatible with setup script & replace pip3 commands with git 
- Move themes, fonts and etc to disk instead?
