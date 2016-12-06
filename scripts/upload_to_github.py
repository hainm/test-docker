#!/usr/bin/env python

import os
import sys
import subprocess

travis = os.getenv('TRAVIS')
travis_os_name = os.getenv('TRAVIS_OS_NAME', '')
travis_branch = os.getenv('TRAVIS_BRANCH', '')
circleci = os.getenv('CIRCLECI', '')
circle_branch = os.getenv('CIRCLE_BRANCH', '')

if circle_branch in ['circleci_py27', 'circleci_py34', 'circleci_py35']:
    commit_message = subprocess.check_output('git log --format=%B |head -2 | tail -1 ', shell=True).decode()
else:
    commit_message = subprocess.check_output('git log --format=%B |head -1', shell=True).decode()

print('git commit message', commit_message)

if not commit_message.startswith("UPLOAD"):
    print("not require to upload. Exit")
    print('Tip: use git commmit -m "UPLOAD: [your_message]" to upload')
    sys.exit(0)

if os.getenv("TRAVIS_PULL_REQUEST") != 'false' or os.getenv('CI_PULL_REQUEST'):
    print("This is a pull request. No deployment will be done")
    sys.exit(0)

if travis:
    if travis_branch != master:
        print("No deployment on {} branch".format(travis_branch))
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
    command_copy = 'cp $HOME/miniconda*/conda-bld/*/amber*bz2 at16/travis/osx-64/'
if circleci:
    command_copy = 'cp $CIRCLE_ARTIFACTS/amber-build/amber*bz2 at16/circleci/linux-64/'

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
else:
    print("skip uploading since travis_os_name is not osx or not using circleci")
