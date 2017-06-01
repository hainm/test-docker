# pytest -vs .

import os
import sys
import subprocess
import unittest
from mock import patch

sys.path.insert(0, '..')
from pack_binary_without_conda_install import pack_non_conda_package

this_dir = os.path.dirname(__file__)
PACK_SCRIPT = os.path.join(this_dir, '..',
                           'pack_binary_without_conda_install.py')
FAKE_TAR = os.path.join(this_dir, 'fake_data', 'fake.tar.bz2')
has_gfortran_local = os.path.exists('/usr/local/gfortran/')


def get_date_label():
    return subprocess.check_output(
        'date +%d%h%y.H%H%M', shell=True).decode().strip()


def test_pack_non_conda_package():
    class Opt():
        pass

    opt = Opt()
    opt.tarfile = FAKE_TAR
    opt.output_dir = '.'
    opt.date = False
    opt.dry_run = False
    with patch('update_gfortran_libs_osx.main') as mock_g_main:
        pack_non_conda_package(opt)
        mock_g_main.assert_called_with(['--copy-gfortran'])


@unittest.skipUnless(has_gfortran_local, 'Must have gfortran in /usr/local')
def test_dry_run():

    # dry run
    cmd = ['python', PACK_SCRIPT, FAKE_TAR, '-d']

    output = subprocess.check_output(cmd).decode()
    assert 'new filename linux-64.fake.tar.bz2' in output


@unittest.skipUnless(has_gfortran_local, 'Must have gfortran in /usr/local')
def test_dry_run_with_date():
    # date
    cmd = ['python', PACK_SCRIPT, FAKE_TAR, '-d', '--date']

    output = subprocess.check_output(cmd).decode()
    line = [
        line for line in output.split('\n')
        if line.startswith('new filename linux')
    ].pop()
    new_fn = line.split()[-1]

    assert len(new_fn.split('.')) == 6
    # e.g: linux-64.fake.01Apr17.H1542.tar.bz2
    assert ('new filename linux-64.fake.{}.tar.bz2'.format(
        get_date_label()) in output)
