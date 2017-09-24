import os
import fix_rpath_osx
from mock import patch
import pytest


amberhome = '/Users/haichit/amber_git/tmp/amber16/'


@pytest.fixture
def amber_src():
    return amberhome


@pytest.fixture
def libcpptraj():
    return os.path.join(amberhome, 'lib', 'libcpptraj.dylib')


def effect(cmd):
    print(cmd)


def test_is_object_file(libcpptraj):
    assert fix_rpath_osx.is_object_file(libcpptraj)
    assert not fix_rpath_osx.is_object_file(__file__)


@patch('os.walk')
@patch('fix_rpath_osx.is_object_file')
def test_get_file_object_from_prefix(mock_obj_file, mock_walk):
    mock_obj_file.return_value = True
    mock_walk.side_effect = [[('1/bin', '', ['cpptraj'])], [('4', '5', ['6.dylib'])]]
    files = list(fix_rpath_osx.get_file_object_from_prefix(amberhome))
    assert files == [os.path.join('1/bin', 'cpptraj'),
                     os.path.join('4', '6.dylib')]


def test_add_loader_path(libcpptraj):
    with patch('subprocess.check_call') as mock_call:
        fix_rpath_osx.add_loader_path(libcpptraj, amberhome, 'lib')
        mock_call.assert_called_with([
            'install_name_tool', '-add_rpath', '@loader_path/../lib',
            libcpptraj
        ])

        mock_call.reset_mock()
        pysander_so = os.path.join(
            amberhome,
            'lib/python3.6/site-packages/sander/pysander.cpython-36m-darwin.so'
        )
        fix_rpath_osx.add_loader_path(pysander_so, amberhome, 'lib')
        mock_call.assert_called_with([
            'install_name_tool', '-add_rpath', '@loader_path/../../../../lib',
            pysander_so
        ])


def test_add_id(libcpptraj):
    with patch('subprocess.check_call') as mock_call:
        fix_rpath_osx.add_id(libcpptraj)
        mock_call.assert_called_with([
            'install_name_tool', '-id', '@rpath/libcpptraj.dylib', libcpptraj
        ])


def test_get_dylibs(libcpptraj):
    expected_libs = sorted([
        '{}/lib/libfftw3.3.dylib'.format(amberhome),
        '{}/lib/libsander.dylib'.format(amberhome),
        '/usr/local/gfortran/lib/libgfortran.3.dylib',
        '/usr/local/gfortran/lib/libstdc++.6.dylib',
        '/usr/local/gfortran/lib/libgcc_s.1.dylib',
        '/usr/lib/libz.1.dylib',
        '/usr/lib/libbz2.1.0.dylib',
        '/usr/lib/libSystem.B.dylib',
    ])
    assert sorted(fix_rpath_osx.get_dylibs(libcpptraj)) == expected_libs


@patch('subprocess.check_call')
def test_get_libs(mock_call, libcpptraj):
    mock_call.side_effect = effect
    libs = fix_rpath_osx.get_dylibs(libcpptraj)
    amber_libs = [lib for lib in libs if amberhome in lib]
    fix_rpath_osx.fix_linking_libs(libcpptraj, amber_libs)


@patch('fix_rpath_osx.add_loader_path')
@patch('fix_rpath_osx.add_id')
@patch('fix_rpath_osx.get_file_object_from_prefix')
@patch('subprocess.check_call')
def test_main(
        mock_call,
        mock_get_files,
        mock_get_id,
        mock_add_loader_path,
        amber_src, libcpptraj):
    mock_get_files.return_value = [os.path.join(amber_src, libcpptraj)]
    fix_rpath_osx.main([amber_src])
    mock_get_id.assert_called_with(libcpptraj)
    mock_add_loader_path.assert_called_with(libcpptraj, amberhome, 'lib')


@patch('fix_rpath_osx.get_file_object_from_prefix')
@patch('subprocess.check_call')
def test_main_with_call(
        mock_call, mock_get_files,
        amber_src, libcpptraj):
    mock_call.side_effect = effect
    mock_get_files.return_value = [os.path.join(amber_src, 'lib', 'libcpptraj.dylib')]
    origin_prefix = '/Users/travis/amber16'
    fix_rpath_osx.main([amber_src, '--prefix', origin_prefix])
