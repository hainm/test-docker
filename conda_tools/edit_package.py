import os
import sys
from glob import glob
import tarfile
import subprocess
from contextlib import contextmanager
import tempfile
import shutil
import json
from shutil import rmtree


def get_package_info(tar_fn):
    # ambertools-17.0-0.tar.bz2
    info_dict = {}
    if not os.path.exists(tar_fn):
        print("Not existing {} yet. Deduce its info from its filename".format(
            tar_fn))
        basename = os.path.basename(tar_fn)
        version = basename.split('-')[1]
        try:
            subdir = tar_fn.split('/')[-2]
            if subdir not in ['linux-64', 'osx-64']:
                subdir = 'unknown'
        except IndexError:
            subdir = 'unknown'
        info_dict['version'] = version
        info_dict['subdir'] = subdir
    else:
        with tarfile.open(tar_fn) as fh:
            m = fh.getmember('info/index.json')
            f = fh.extractfile(m)
            content = f.read().decode()
            info_dict = json.loads(content)
    return info_dict


def get_date_label():
    return subprocess.check_output(
        'date +%d%h%y.H%H%M', shell=True).decode().strip()


@contextmanager
def editing_conda_package(pkg_name,
                          output_dir='./tmp',
                          prefix=None,
                          add_date=True,
                          dry_run=False,
                          conda=False):
    ''' do something with `pkg_name` and write a new conda package to `output_dir`

    Parameters
    ----------
    pkg_name : str, conda-build package name (e.g: ambertools-17.0.1-py35_1.tar.bz2)
    output_dir : str, directory that stores new tar file
    prefix : None or str
        if given, create a new name {prefix}.pkg_name
    add_date : bool, default True
        if True, add date information to package name.
    conda : bool, default False
        if True, output tarfile will be a conda package, else non-conda package.
        The difference is that non-conda package has $PREFIX/amber{version}/{info, ...}
        while conda package has $PREFIX{info, ...}
    '''
    pkg_name_path = os.path.abspath(pkg_name)
    basename = os.path.basename(pkg_name)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_dir = os.path.abspath(output_dir)
    cwd = os.getcwd()
    os.chdir(output_dir)

    package_info = get_package_info(pkg_name_path)
    # ambertools-17.0-0.tar.bz2
    amber_version = package_info.get('version').split('.')[0]
    amber_folder = 'amber{}'.format(amber_version)
    platform = package_info['subdir']

    if add_date:
        date_str = get_date_label() + '.'
    else:
        date_str = ''
    if prefix is not None:
        new_fn = prefix + '.' + basename.replace('tar.bz2',
                                                 '') + date_str + 'tar'
    else:
        new_fn = platform + '.' + basename.replace('tar.bz2',
                                                   '') + date_str + 'tar'
    if conda:
        new_fn = os.path.basename(pkg_name.replace('.bz2', ''))

    print('date_str', date_str)
    print('new filename', new_fn + '.bz2')
    # if you change "Absolute filename dir", make sure to update
    # it in build_all.py too
    # TODO: more reliable checking?
    print('ABSOLUTE FILENAME DIR {}'.format(
        os.path.join(output_dir, new_fn + '.bz2')))
    print('package_info', package_info)
    print('amber_version', amber_version)

    with tempfolder():
        if not dry_run:
            with tarfile.open(pkg_name_path) as fh:
                fh.extractall(path='.')

            yield  # do something here

            others = [os.path.basename(fn) for fn in glob('*')]
            tmp_dir = os.getcwd()

            # create symlink so all folder in $AMBERHOME will go to amber{version}/ folder
            subprocess.check_call(['ln', '-s', tmp_dir, amber_folder])

            all_files_in_amber = [
                os.path.join(amber_folder, fn) for fn in others
            ] if not conda else others

            commands = ['tar', '-cf', new_fn] + all_files_in_amber
            subprocess.check_call(commands)

            subprocess.check_call(['bzip2', '-z', new_fn])
            shutil.copy(new_fn + '.bz2', output_dir)
        else:
            yield
            print("Dry run: Not doing actually untar")

    os.chdir(cwd)


@contextmanager
def tempfolder():
    my_temp = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(my_temp)
    yield
    os.chdir(cwd)
    rmtree(my_temp)


if __name__ == '__main__':
    # main_update_registration()
    print(get_package_info(sys.argv[1]))
