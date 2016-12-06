#!/usr/bin/env python

import os
import subprocess

# TODO: python
travis_os_name = os.getenv('TRAVIS_OS_NAME', '')
circleci = os.getenv('CIRCLECI', '')

if travis_os_name:
    subprocess.check_call('source scripts/check_deployment.sh', shell=True)

commands_init = """
    git clone ${MYREPO_URL}
    cd $MYREPO 
    git config user.name $MYUSER
    git config user.email $MYEMAIL
""".strip().split('\n')

command_copy = 'echo'
# ovewrite command_copy
if travis_os_name:
    command_copy = 'cp $HOME/miniconda*/conda-bld/*/amber*bz2 at16/'
if circleci:
    command_copy = 'cp $CIRCLE_ARTIFACTS/amber-build/amber*bz2 at16/'

commands_add_and_push = """
    git add at16/amber*bz2
    git commit -m 'push to github'
    git remote add production https://${GITHUB_TOKEN}@github.com/$MYUSER/$MYREPO >& log
    git push production master --force >& log
""".strip().split('\n')

if travis_os_name == 'osx' or circleci:
    for command in commands_init:
        subprocess.check_call(command, shell=True)
    subprocess.check_call(command_copy, shell=True)
    for command in commands_add_and_push:
        subprocess.check_call(command, shell=True)
