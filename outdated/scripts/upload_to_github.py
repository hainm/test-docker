#!/usr/bin/env python

# For travis upload

import os
import sys
import subprocess

travis_os_name = os.getenv('TRAVIS_OS_NAME', '')
travis_branch = os.getenv('TRAVIS_BRANCH', '')
travis_pull_request = os.getenv('TRAVIS_PULL_REQUEST', '')

# DEBUG
# travis_os_name = 'osx'
# travis_branch = 'master'
# travis_pull_request = 'false'

commit_message = subprocess.check_output('git log --format=%B |head -1', shell=True).decode()

print('git commit message', commit_message)

if travis_branch != 'master':
    print("No deployment on {} branch".format(travis_branch))
    sys.exit(0)

if travis_pull_request != 'false':
    print("This is a pull request. No deployment will be done")
    sys.exit(0)

commands_init = """
    git clone ${MYREPO_URL}
    echo 'my repo' $MYREPO
    cd $MYREPO 
    git config user.name $MYUSER
    git config user.email $MYEMAIL
    git checkout gh-pages
    git pull origin gh-pages
""".strip().split('\n')


commands_copy_and_update_index = [
    'for at in $HOME/TMP/amber-conda-bld/*/* ; do '
    'cp $at at17/; done'
]

commands_add_and_push = """
    git add at17/*
    git commit -m 'push to github'
    git remote add production https://${GITHUB_TOKEN}@github.com/$MYUSER/$MYREPO
    git push production gh-pages --force
""".strip().split('\n')

all_commands = commands_init + commands_copy_and_update_index + commands_add_and_push
all_commands_string = ' && '.join(all_commands)
# print(all_commands_string)

print(all_commands_string)

if travis_os_name == 'osx':
    subprocess.call(all_commands_string, shell=True)
else:
    print("skip uploading since travis_os_name is not osx or not using circleci")
