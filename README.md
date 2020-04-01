# auto-dev-setup

Python script to replicate personal development environment across any machine 
with proper packaging, editor profiles & settings. OSX machine environment
 only. This is currently partially personalized to my settings, feel free to
  use, fork or extend this however you wish.

# Requirements
- `Python3` to run the executable scripts
- Latest version of `pip3` otherwise the script requires a second run to
 complete
    - Run `pip3 install -r requirements` to fetch all script dependencies
         after installing pip3
- To communicate with the GitHub API, add `config/git-credentials.txt` in the 
project if it doesn't exist (otherwise the script generates it for you upon 
initial setup execution which will prompt you to configure this before 
proceeding) 
    - e.g. `config/git-credentials.txt`
    ```text 
      username: vilst3r
      email: clifford.phan@gmail.com
      token: ****************************************  <- personal_access_token
    ```
    - For your personal access token, you can generate this under 
    `Developer settings` on [GitHub](https://github.com/settings/tokens)

# Optional (Personalizing your settings)
- `config/brew/brew.txt`: will contain all the brew packages delimited by
 the newline character.
    - See the [Brew registry](https://formulae.brew.sh/formula/) for the list
     of OSX binaries that are available
    - E.g. `config/brew/brew.txt`
    ```text 
    python
    go
    git
    postgresql
    node
    docker
    vim
    gcc
    ```
    
- `config/brew/brew-cask.txt`: Similarly will contain all the cask
 packages delimited by the newline character.
    - See the [Cask registry](https://formulae.brew.sh/cask/) for the list of
     system applications that are available
    - E.g. `config/brew/brew-cask.txt`
    ```text 
    docker
    emacs
    google-chrome
    google-drive-file-stream
    intellij-idea-ce
    iterm2
    microsoft-office
    postman
    pycharm-ce
    slack
    spotify
    sublime-text
    visual-studio-code
    ```
- A `dotfiles` git repository to take advantage of vim, bash & emac
 configurations. As long as you have that specific github repository name &
  the following three files:
    - `.bash_profile`
    - `.vimrc`
    - `.emacs`
- Then the script program will automatically set these configs for you with
 the `powerline` package from pip3

# How to use
- After configuring your packages & etc, to install your configured 
environment, simply just run: `./setup` & provide your user password (needs
 to be an admin) when prompted in order to automate the processes within the 
 script.
- To clean up the work of the script, run `./cleanup` & enter your password
 as well for the script to automate processes


# Automated Process Summary
1. Configures your SSH settings to hook into GitHub
2. Installs the homebrew binary 
3. Installs all brew packages from './config/brew/brew.txt'
4. Installs all cask packages from './config/brew/brew-cask.txt'
5. (Optional) As fore mentioned, if your GitHub account contains the repository
 `dotfiles`, then it'll pull that file & configure your vim, bash & emacs
  settings
6. Installs the powerline-status & configures it accordingly with your vim
 & bash settings

# Notes & Issues
- Password is required when OS X prompts you to enter your password for the 
    keychain access, choosing 'Always Allow' would make the whole process 
    seamless without any prompts from then onwards
- If any issues arises during the process, log output is available to diagnose
 for either `logs/setup/*.log` or `logs/clean/*.log` & run `./cleanup` to
  undo automated installations

# TODO (potentially)
- Add iTerm2 configuration in spare time in the future
- Add C++ bits/header to setup
