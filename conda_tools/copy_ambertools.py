#!/usr/bin/env python
import os
import subprocess
from glob import glob

extra_folders_or_files = ['AmberTools/test/dacdif']
excluded_folders = [
    '../../../test', 'AmberTools/test', 'AmberTools/examples',
    'AmberTools/benchmark'
]

this_path = os.path.abspath(os.path.dirname(__file__))


def mkdir_ambertree():
    for folder in [
            'dat', 'doc', 'AmberTools', 'AmberTools/src', 'AmberTools/test'
    ]:
        try:
            os.mkdir(folder)
        except OSError:
            pass


def _having_one_of_them(name, word_set):
    for word in word_set:
        if word in name:
            return True
    return False


def _copy_folder(source_dir, target_dir):
    subprocess.call(['cp', '-r', source_dir, target_dir])


def copy_tree(dry_run=False):
    # use mkrelease_at as a file source
    recipe_dir = os.getenv('RECIPE_DIR',
                           os.path.join(this_path, '../conda-ambertools-single-python'))
    print('recipe_dir', recipe_dir)
    print('this_path', this_path)
    amberhome = os.path.abspath(os.getenv('AMBER_SRC'))
    print('recipe_dir', recipe_dir)
    print('amberhome', amberhome)
    assert os.path.exists(recipe_dir)
    assert os.path.exists(amberhome)
    assert os.path.exists(os.path.join(amberhome, 'AmberTools'))

    mkrelease_at_file = os.path.join(amberhome, 'mkrelease_at')
    if os.path.exists(mkrelease_at_file):
        mkdir_ambertree()
        # development version
        extra_dirs = [
            os.path.join(amberhome, folder)
            for folder in extra_folders_or_files
        ]

        for source_dir in extra_dirs:
            target_dir = os.path.join('AmberTools', 'src')
            print('copying {} to {}'.format(source_dir, target_dir))
            if not dry_run:
                _copy_folder(source_dir, target_dir)

        with open(mkrelease_at_file) as fh:
            for line in fh.readlines():
                line = line.strip()
                if line.startswith('$TAR'):
                    folder_or_folders = line.split('/')[-1]
                    if '{' in folder_or_folders:
                        # list of folders
                        # {x,y,z}
                        folders = folder_or_folders.replace('{', '').replace(
                            '}', '').split(',')
                    else:
                        # single folder
                        folders = [
                            folder_or_folders,
                        ]
                    root_dir = '/'.join(line.split('/')[1:-1])

                    for folder in folders:
                        if not root_dir:
                            source_dir = os.path.join(amberhome, folder)
                            target_dir = '.'
                        else:
                            source_dir = os.path.join(amberhome, root_dir,
                                                      folder)
                            target_dir = root_dir
                        if not _having_one_of_them(source_dir,
                                                   excluded_folders):
                            files = glob(source_dir)
                            print('copying {} to {}'.format(
                                source_dir, target_dir))
                            if not os.path.exists(source_dir):
                                print(
                                    'WARNING NOT FOUND: {}'.format(source_dir))
                            if not os.path.exists(target_dir):
                                print('WARNING NOT FOUND target_dir: {}'.
                                      format(target_dir))
                            assert os.path.exists(target_dir)
                            if not dry_run:
                                for fn in files:
                                    _copy_folder(fn, target_dir)
    else:
        print(
            "not having mkrelease_at in AMBERHOME={}, assume this is a released version".
            format(amberhome))
        for fn in glob(amberhome + '/*'):
            cmd = ['cp', '-r', fn, '.']
            print(' '.join(cmd))
            if not dry_run:
                _copy_folder(fn, '.')


def main():
    copy_tree()


if __name__ == '__main__':
    copy_tree(dry_run=True)
