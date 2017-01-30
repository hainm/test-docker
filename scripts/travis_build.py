import os
import sys
from subprocess import check_call, check_output

travis_os_name = os.getenv('TRAVIS_OS_NAME', '')
python_version = os.getenv('PYTHON_VERSION')
travis_branch = os.getenv('TRAVIS_BRANCH')
commit_message = check_output('git log --format=%B |head -1', shell=True).decode()

if (travis_branch.startswith('circleci_') or
    travis_branch.startswith('appveyor')):
    print("This {} brach will not be run on travis. Skip".format(travis_branch))
    sys.exit(0)
elif '[skip build]' in commit_message.lower():
    print(commit_message)
    sys.exit(0)
elif '[circleci only]' in commit_message:
    print('skip travis due to [circleci only] flag')
    sys.exit(0)
else:
    if travis_os_name == 'osx':
        check_call('brew tap homebrew/science', shell=True)
        check_call('brew update', shell=True)

        # turn off since we are using /usr/local/gfortran/
        # check_call('brew install gcc', shell=True)
    if travis_os_name == 'linux':
        check_call('sudo apt-get install -y csh', shell=True)
    check_call('source scripts/install_miniconda.sh', shell=True)
    check_call('$HOME/miniconda3/bin/conda build recipe --py {}'.format(python_version), shell=True)
