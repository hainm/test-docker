# pytest -vs .

import os
import sys
from mock import patch
import shutil

sys.path.insert(0, '..')
from fix_conda_gfortran_linking_osx import repack_conda_package, main

this_dir = os.path.dirname(__file__)
PACK_SCRIPT = os.path.join(this_dir, '..',
                           'pack_binary_without_conda_install.py')
FAKE_TAR = os.path.join(this_dir, 'fake_data', 'fake_osx.tar.bz2')
has_gfortran_local = os.path.exists('/usr/local/gfortran/')


def test_repack_conda_package():
    class Opt():
        pass

    opt = Opt()
    opt.tarfile = FAKE_TAR
    opt.output_dir = '.'
    opt.date = False
    opt.dry_run = False
    with patch('update_gfortran_libs_osx.main') as mock_g_main:
        repack_conda_package(opt)
        mock_g_main.assert_called_with([])
    os.remove(os.path.basename(FAKE_TAR))


def test_main():
    junk = './tmp_fdasfda'
    output_dir = '{}/heyhey'.format(junk)
    main([FAKE_TAR, '-o', output_dir])
    assert os.path.exists(os.path.join(output_dir, os.path.basename(FAKE_TAR)))
    shutil.rmtree(junk)
