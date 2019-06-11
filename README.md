# env-setup

Python scripts to replicate personal development environment across any machine with proper packaging and editor profiles and settings. Linux machine environment only.

# Process
1. Configure git ssh key (requires passcode)
2. Installs homebrew (requires passcode)
3. Installs brew packages from './config/brew.txt'
4. Installs brew cask software from './config/brew-cask.txt'
5. Install & Configure vim
6. Install & Configure bash
7. Install powerline
...

# Todo
- Setup OAuth for authorization instead of authentication to integrate this script applicaiton for GitHub
- Make API call to GitHub to add SSH Key for local machine
- Consolidate the powerline configurations with the fonts and styling applied
- Configure iterm2 profile somehow...
