# env-setup

Python scripts to replicate personal development environment across any machine with proper packaging and editor profiles and settings. Linux machine environment only.

# Requirements
- Python 3 system binary installed to run the script
- Requests library for the script to interact with GitHub API (pip3 install requests)
- Configure 'git-credentials.txt' with username, email & oath token properties delimited by a colon

# Process
1. Configure git ssh key (requires passcode)
2. Installs homebrew (requires passcode)
3. Installs brew packages from './config/brew.txt'
4. Installs brew cask software from './config/brew-cask.txt'
5. Install & Configure vim
6. Install & Configure bash
7. Install & Configure powerline
...

# Todo
- Write e2e/integration tests or test it manually?
- Fix up pathing & imports in project
- Add requirements.txt
- Isolate to virtualenv
- Consolidate the powerline configurations with the fonts and styling applied
- Configure iterm2 profile somehow...
