#!/usr/bin/env python

import os
import subprocess

# TODO: python
subprocess.check_call('source scripts/check_deployment.sh', shell=True)
travis_os_name = os.getenv('TRAVIS_OS_NAME', '')
circleci = os.getenv('CIRCLECI', '')

commands = """
    git clone ${MYREPO_URL}
    cd $MYREPO 
    git config user.name $MYUSER
    git config user.email $MYEMAIL
    cp $HOME/miniconda*/conda-bld/*/amber*bz2 at16/
    git add at16/amber*bz2
    # cp $HOME/miniconda*/conda-bld/*/test*bz2 .
    # git add test*bz2
    git commit -m 'push to github'
    git remote add production https://${GITHUB_TOKEN}@github.com/$MYUSER/$MYREPO >& log
    git push production master --force >& log
""".strip().split('\n')

if travis_os_name == 'osx' or circleci:
    for command in commands:
        subprocess.check_call(command, shell=True)
