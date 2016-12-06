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
    echo 'my repo' $MYREPO
    cd $MYREPO 
    git config user.name $MYUSER
    git config user.email $MYEMAIL
    ls .
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
    git remote add production https://${GITHUB_TOKEN}@github.com/$MYUSER/$MYREPO
    git push production master --force
""".strip().split('\n')

all_commands = commands_init + [command_copy,] + commands_add_and_push
all_commands_string = ' && '.join(all_commands)
print(all_commands_string)

if travis_os_name == 'osx' or circleci:
    subprocess.call(all_commands_string, shell=True)
