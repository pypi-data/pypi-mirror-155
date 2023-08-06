
# Welcome to Pyconfig
Dotfiles is a repo for managing dotfiles. The idea is to collect those time-consuming files to setup in one directory and reference them via symbolic links from there original locations. Thus, when a new machine is required to be setup, all that is required to clone the repo in that machine and create the symbolic links.

Dotfiles include, but are not limited to:
* `~/.gitconfig`
* `~/.ssh`
* `~/.aws`
* `~/.bash_profile`
* `~/.bashrc`
* `$profile` in Windows Powershell
* etc

Additionally, files that contain data, sensitive information that should not be pushed to a repository are contained in a directory `~/dotfiles`. The files therein are encrypted before backedup.

Additionally, scripts to perform setup of new machines and perform mundane tasks are maintained here in `scripts`. The repo uses Python to perform the tasks.

