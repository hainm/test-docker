#!/usr/bin/env python

import os
import sys
import subprocess

travis = os.getenv('TRAVIS')
travis_os_name = os.getenv('TRAVIS_OS_NAME', '')
circleci = os.getenv('CIRCLECI', '')

if os.getenv("TRAVIS_PULL_REQUEST") == 'false' or os.getenv('CI_PULL_REQUEST'):
    print("This is a pull request. No deployment will be done")
    sys.exit(0)

if travis:
    if os.getenv("TRAVIS_BRANCH") != "master":
        print("No deployment on BRANCH='$TRAVIS_BRANCH'")
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

command_copy = 'echo'
# ovewrite command_copy
if travis_os_name:
    command_copy = 'cp $HOME/miniconda*/conda-bld/*/amber*bz2 at16/travis/'
if circleci:
    command_copy = 'cp $CIRCLE_ARTIFACTS/amber-build/amber*bz2 at16/circleci/'

commands_add_and_push = """
    git add at16/*
    git commit -m 'push to github'
    git remote add production https://${GITHUB_TOKEN}@github.com/$MYUSER/$MYREPO
    git push production gh-pages --force
""".strip().split('\n')

all_commands = commands_init + [command_copy,] + commands_add_and_push
all_commands_string = ' && '.join(all_commands)
# print(all_commands_string)

if travis_os_name == 'osx' or circleci:
    subprocess.call(all_commands_string, shell=True)
