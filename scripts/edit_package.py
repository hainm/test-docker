import os
from glob import glob
import tarfile
import subprocess

import os
from contextlib import contextmanager
import tempfile
import shutil
from shutil import rmtree
import conda
from conda.cli.main_package import make_tarbz2

@contextmanager
def editing_conda_package(pkg_name, output_dir='./tmp'):
    ''' do something with `pkg_name` and write a new conda package to `output_dir`
    '''
    pkg_name_path = os.path.abspath(pkg_name)
    basename = os.path.basename(pkg_name)
    assert basename.endswith('.bz2'), 'must be a conda package with .bz2 extension'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_dir = os.path.abspath(output_dir)
    cwd = os.getcwd()
    os.chdir(output_dir)
    with tempfolder():
        with tarfile.open(pkg_name_path) as fh:
            fh.extractall(path='.')
        yield # do something here
        new_fn = basename.strip('\.bz2')
        others = glob('*')
        commands = ['tar', '-cf', new_fn] + others
        subprocess.call(commands)
        subprocess.call(['bzip2', '-z', new_fn])
        subprocess.call(['ls'])
        shutil.copy(basename, output_dir)
    os.chdir(cwd)

@contextmanager
def tempfolder():
    my_temp = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(my_temp)
    yield
    os.chdir(cwd)
    rmtree(my_temp)

def main_update_registration():
    version = '16.20'
    build_number = 1

    for py_version in ['27', '34', '35']:
        basename = ('ambermini101-{version}-py{py_version}_{build_number}.tar.bz2'
                    .format(version=version, build_number=build_number,
                            py_version=py_version))
        tar_fn = os.path.abspath(basename)
        reg_file = '/Users/haichit/amber_git/ambertools-conda-build/recipe/amber_registration.py'
        reg_file_in_tarfile = 'bin/amber_registration'

        with editing_conda_package(pkg_name=basename, output_dir='./tmp'):
            shutil.copyfile(reg_file, reg_file_in_tarfile)

if __name__ == '__main__':
    main_update_registration()
