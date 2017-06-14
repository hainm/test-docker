import os
import sys
import tempfile
import subprocess
from mock import patch
from contextlib import contextmanager
from shutil import rmtree

this_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(this_dir, '..'))
BUILD_SCRIPT = os.path.join(this_dir, '..', 'build_all.py')

# ../
import build_all
import utils


@contextmanager
def tempfolder():
    my_temp = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(my_temp)
    yield
    os.chdir(cwd)
    rmtree(my_temp)


@patch('subprocess.check_call')
def test_build_all_main(check_call):
    build_all.main([])


def test_build_all_cmd():
    cmd = ['python', BUILD_SCRIPT, '-d']
    with tempfolder():
        subprocess.check_call(cmd)

    cmd = ['python', BUILD_SCRIPT, '-d', '--exclude-osx']
    with tempfolder():
        subprocess.check_call(cmd)

    cmd = ['python', BUILD_SCRIPT, '-d', '--exclude-linux']
    with tempfolder():
        subprocess.check_call(cmd)

    cmd = ['python', BUILD_SCRIPT, '-d', '--no-docker']
    with tempfolder():
        subprocess.check_call(cmd)


def test_build_all_cmd_with_assertion():
    package = os.path.basename(
        utils.get_package_dir(
            os.path.join(this_dir, '..', '..',
                'conda-ambertools-all-python')))
    print('package', package)
    all_lines = [
        'amber-conda-bld/osx-64/{}'.format(package),
        'amber-conda-bld/linux-64/{}'.format(package),
        'amber-conda-bld/non-conda-install/osx-64.{}'.format(package),
        'amber-conda-bld/non-conda-install/linux-64.{}'.format(package),
    ]

    cmd = ['python', BUILD_SCRIPT, '-d']
    with tempfolder():
        tdir = os.getcwd()
        expected_lines = [os.path.join(tdir, line) for line in all_lines]

        output = subprocess.check_output(cmd).decode()
        print('output', output)

        lines = [line for line in output.split('\n') if line][-4:]
        print('lines', lines)

        assert expected_lines == lines
