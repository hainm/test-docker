import os
from glob import glob
import subprocess
import argparse


def main(args=None):
    """Fix rpath for .dylib, executable and Python extension .so files
    """
    # root might be bin, lib, ...
    parser = argparse.ArgumentParser()
    parser.add_argument('in_dir')
    opt = parser.parse_args(args)

    files = [
        fn for fn in glob(os.path.join(opt.in_dir, '*'))
        if os.path.isfile(fn) and not fn.endswith('.a')
    ]

    # get path-nested so files
    files.extend(get_so_files(opt.in_dir))

    for target in files:
        lib_paths = [
            lib_path for lib_path in get_dylibs(target) if 'conda' in lib_path
        ]
        if target.endswith('dylib'):
            update_id(target)
        if lib_paths:
            fix_linking_libs(target, lib_paths)


def get_dylibs(fn):
    # get_dylibs('libcpptraj.dylib')
    # return a list of files that `fn` linked to.
    commands = ['otool', '-L', fn]
    try:
        subprocess.check_call(commands)
    except subprocess.CalledProcessError:
        return []

    output = subprocess.check_output(commands).decode()
    lines = [line.split()[0] for line in output.split('\n') if line]
    if fn.endswith('dylib'):
        # exclude its ID
        return lines[2:]
    else:
        return lines[1:]


def update_id(lib_path):
    # change to @rpath instead of using absolute path
    basename = os.path.basename(lib_path)
    subprocess.check_call(
        'install_name_tool -id @rpath/{} {}'.format(basename, lib_path),
        shell=True)


def fix_linking_libs(target, lib_paths):
    # change to @rpath instead of using absolute path
    for lib_path in lib_paths:
        basename = os.path.basename(lib_path)
        subprocess.check_call([
            'install_name_tool', '-change', lib_path,
            '@rpath/{}'.format(basename), target
        ])


def get_needed_to_be_fixed_libs():
    # any file having 'conda' keyword from 'otool -L'
    need_tobe_fixed_libs = []
    for lib in glob('*.dylib'):
        for linked_lib in get_dylibs(lib):
            if 'conda' in linked_lib:
                need_tobe_fixed_libs.append(linked_lib)
                break


def get_so_files(root):
    # all python extensions needed to be fixed
    level = 6
    all_so_files = []
    python_package_root = os.path.join(root, 'python*', 'site-packages', '*')

    for index in range(level):
        path_pattern = os.path.join(python_package_root, '/'.join('*' * index),
                                    '*.so')
        print('pattern', path_pattern)
        so_file_paths = glob(path_pattern)
        all_so_files.extend(so_file_paths)
    return all_so_files


if __name__ == '__main__':
    main()
