import os
from subprocess import check_call

travis_os_name = os.getenv('TRAVIS_OS_NAME', '')
python_version = os.getenv('PYTHON_VERSION')
travis_branch = os.getenv('TRAVIS_BRANCH')

if not travis_branch.startswith('circleci_'):
    if travis_os_name == 'osx':
        check_call('brew tap homebrew/science', shell=True)
        check_call('brew update', shell=True)
        check_call('brew install gcc', shell=True)
    if travis_os_name == 'linux':
        check_call('sudo apt-get install -y csh', shell=True)
    check_call('source scripts/install_miniconda.sh', shell=True)
    check_call('conda build recipe --py {}'.format(python_version), shell=True)
else:
    print("This {} brach will not be run on travis. Skip")
