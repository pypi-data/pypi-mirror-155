# Todopy
An implementation of [todo.txt](http://todotxt.org/) in python3.9. It has the following features:

- git integration
- `todo stale` integration
- tree views 
- hiding tasks for a certain number of days using `todo schedule` .


## Installation
First, clone the repository to a folder of your choice (For example: `~/bin/todotree`).

Then, copy `config.ini.default` to `config.ini` and make the necessary changes to suit your needs. 

If you want to use `git` to keep track of the changes, you need to do the following:

- Change the url to your own private git repo: `git remote set-url origin <new_url>`
- Delete either the `.gitignore` or remove the `config.ini` line. This allows your config to be tracked by git. 

## Environment Variables used

- `EDITOR` os editor. `nano` or `vim` are obvious choices. If you are on Windows, you'll want to use `code` to open it in vscode.

## Used external Programs

- `date` (optional) from `coreutils` for `schedule`, this allows you to do something like `todo schedule 13 tomorrow`, instead of having to use ISO dates (2021-02-14).
- `git` (optional), for using a git repository.

## Bash autocompletion

You can activate bash autocompletion with `source todo.completions.bash` after cloning.
Add this to your `~.bashrc` so that it always is available.

## Screenshots

projecttree

![projecttree](projecttree-example.png) 

contexttree

![contexttree](contexttree-example.png)
