import sys
import os
import pytest
import subprocess
from mock import patch, MagicMock

sys.path.insert(0, '..')
import update_gfortran_libs_osx as ugo

EXPECTED_DEPS = [
    '/usr/local/gfortran/lib//libstdc++.6.dylib',
    '/usr/local/gfortran/lib//libgfortran.3.dylib',
    '/usr/local/gfortran/lib//libgcc_s.1.dylib',
    '/usr/local/gfortran/lib//libquadmath.0.dylib',
]


@pytest.fixture
def gfortran_dylib():
    return '/usr/local/gfortran/lib//libgfortran.3.dylib'


def test_get_dylibs(gfortran_dylib):
    expected = [
        '/usr/local/gfortran/lib/libgfortran.3.dylib',
        '/usr/local/gfortran/lib/libquadmath.0.dylib',
        '/usr/lib/libSystem.B.dylib',
        '/usr/local/gfortran/lib/libgcc_s.1.dylib'
    ]
    assert ugo.get_dylibs(gfortran_dylib) == expected


@patch('os.makedirs')
@patch('update_gfortran_libs_osx.update_rpath')
@patch('update_gfortran_libs_osx.copy_gfortran_libs')
def test_main(mock_copy_gfortran_libs, mock_update_rpath, mock_mkdir):
    ugo.main(['.', '--copy-gfortran'])
    prefix = '.'
    g_dest = os.path.join(prefix, 'lib', 'amber_3rd_party')
    mock_update_rpath.assert_called_with(
        prefix, g_dest=g_dest, copy_gfortran=True)
    mock_mkdir.assert_called_with(g_dest)
    mock_copy_gfortran_libs.assert_called_with(
        dest=g_dest, g_dir='/usr/local/gfortran/lib')


def test_get_dependence():
    deps = ugo.get_dependence('/usr/local/gfortran/lib/libgfortran.3.dylib')
    assert deps == [
        '/usr/local/gfortran/lib/libgfortran.3.dylib',
        '/usr/local/gfortran/lib/libquadmath.0.dylib',
        '/usr/local/gfortran/lib/libgcc_s.1.dylib'
    ]


@patch('subprocess.check_output')
@patch('update_gfortran_libs_osx.get_dependence')
def test_get_so_files(mock_get_dependence, mock_check_output):
    mock_check_output.return_value = b"""./lib/libsaxs_md.so
./lib/libsaxs_rism.so
./lib/python2.7/site-packages/parmed/amber/_rdparm.so
./lib/python2.7/site-packages/pytraj/analysis/c_action/actionlist.so
./lib/python2.7/site-packages/pytraj/analysis/c_action/c_action.so"""

    def glob_side_effect(pattern):
        d = {
            './bin/*': ['./bin/cpptraj'],
            './bin/to_be_dispatched/*': ['./bin/to_be_dispatched/teLeap'],
            './lib/*dylib': ['./lib/libsander.dylib']
        }
        return d[pattern]

    def isfile_effect(fn):
        return fn.endswith('.so') or fn.endswith('.dylib')

    mock_get_dependence.return_value = True

    with patch('glob.glob') as mock_glob:
        mock_glob.side_effect = glob_side_effect
        output = mock_check_output.return_value.decode('utf-8')
        so_files = ugo.get_so_files('.')
        assert so_files == output.split('\n')

        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.side_effect = isfile_effect
            will_be_fixed = ugo.get_will_be_fixed_files('.')
            print('will_be_fixed', will_be_fixed)
        assert will_be_fixed == [
            './lib/libsaxs_md.so',
            './lib/libsaxs_rism.so',
            './lib/python2.7/site-packages/parmed/amber/_rdparm.so',
            './lib/python2.7/site-packages/pytraj/analysis/c_action/actionlist.so',
            './lib/python2.7/site-packages/pytraj/analysis/c_action/c_action.so',
            './lib/libsander.dylib'
        ]


@patch('subprocess.check_call')
@patch('update_gfortran_libs_osx.add_rpath')
@patch('update_gfortran_libs_osx.get_dependence')
@patch('update_gfortran_libs_osx.get_dylibs')
@patch('update_gfortran_libs_osx.get_will_be_fixed_files')
def test_update_rpath(mock_will_be_fixed_files, mock_get_dylib,
                      mock_get_dependence, mock_add_rpath, mock_check_call):
    mock_get_dependence.return_value = EXPECTED_DEPS
    mock_will_be_fixed_files.return_value = [
        'lib/python2.7/site-packages/pytraj/trajectory/frame.so',
        'lib/libsander.dylib', 'bin/cpptraj'
    ]
    ugo.update_rpath('.')
    mock_add_rpath.assert_called_with('bin/cpptraj',
            '@loader_path/../lib/amber_3rd_party')


def test_copy_gfortran_libs():
    expected = [('/usr/local/gfortran/lib//libstdc++.6.dylib',
                 'lib/amber_3rd_party'),
                ('/usr/local/gfortran/lib//libgfortran.3.dylib',
                 'lib/amber_3rd_party'),
                ('/usr/local/gfortran/lib//libgcc_s.1.dylib',
                 'lib/amber_3rd_party'),
                ('/usr/local/gfortran/lib//libquadmath.0.dylib',
                 'lib/amber_3rd_party')]

    with patch('shutil.copy'):
        file_pairs = ugo.copy_gfortran_libs(dest='lib/amber_3rd_party')
        assert file_pairs == expected


@patch('subprocess.check_call')
def test_change_to_rpath_dot_lib(mock_check_call):
    dep = 'my/libgfortran.3.dylib'
    fn = 'bin/cpptraj'
    cmd = ugo.change_to_rpath_dot_lib(dep, fn)
    assert cmd == 'install_name_tool -change my/libgfortran.3.dylib @rpath/amber_3rd_party/libgfortran.3.dylib bin/cpptraj'
    args = cmd.split()
    mock_check_call.assert_called_with(args)
