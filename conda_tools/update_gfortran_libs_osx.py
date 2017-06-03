'''This script will
- copy gfortran-related to lib/amber_3rd_party folder and fix the rpath
- Link lib/*.dylib and bin/{cpptraj, mdgx, ...} to that lib/amber_3rd_party folder
'''

import os
import sys
import shutil
import glob
import argparse
import subprocess

required_libs = [
    'libstdc++.6.dylib', 'libgfortran.3.dylib', 'libgcc_s.1.dylib',
    'libquadmath.0.dylib'
]


def get_dylibs(fn):
    output = subprocess.check_output(['otool', '-L', fn]).decode()
    lines = [line.split()[0] for line in output.split('\n') if line]
    return lines[1:]


# Note: we port conda-build "add_rpath" here to avoid adding conda-build
# as a requirement (got some weird errros if doing so.)
def add_rpath(path, rpath, verbose=False):
    # from conda-build
    # BSD-3: https://github.com/conda/conda-build/blob/master/LICENSE.txt
    """Add an `rpath` to the Mach-O file at `path`"""
    args = ['install_name_tool', '-add_rpath', rpath, path]
    if verbose:
        print(' '.join(args))
    p = subprocess.Popen(args, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    stderr = stderr.decode('utf-8')
    if "Mach-O dynamic shared library stub file" in stderr:
        print("Skipping Mach-O dynamic shared library stub file %s\n" % path)
        return
    elif "would duplicate path, file already has LC_RPATH for:" in stderr:
        print("Skipping -add_rpath, file already has LC_RPATH set")
        return
    else:
        print(stderr)
        if p.returncode:
            raise RuntimeError(
                "install_name_tool failed with exit status %d" % p.returncode)


# assume you are in $AMBERHOME
def get_will_be_fixed_files():
    so_files = get_so_files()
    return [
        fn
        for fn in so_files + glob.glob('bin/*') + glob.glob(
            'bin/to_be_dispatched/*') + glob.glob('lib/*dylib')
        if get_dependence(fn)
    ]


def get_so_files(dest='.'):
    output = subprocess.check_output(
        'find {} -type f -name "*.so"'.format(dest), shell=True)
    output = output.decode()
    return [fn for fn in output.split('\n') if fn]


def copy_gfortran_libs(g_dir='/usr/local/gfortran/lib/', dest='.'):
    file_pairs = []
    for fn in required_libs:
        src = g_dir + '/' + fn
        shutil.copy(src, dest)
        file_pairs.append((src, dest))
    return file_pairs


def get_dependence(orig_lib):
    p = subprocess.Popen(
        ['otool', '-L', orig_lib],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    _, err = p.communicate()
    err = err.decode()

    if ('The file was not recognized as a valid object file' in err or
            'Is a directory' in err):
        return []
    else:
        return [
            lib for lib in get_dylibs(orig_lib)
            if lib.startswith('/usr/local/gfortran/lib/')
        ]


def change_to_rpath_dot_lib(dep, fn):
    basename = os.path.basename(dep)
    cmd = [
        'install_name_tool', '-change', dep,
        '@rpath/amber_3rd_party/{}'.format(basename), fn
    ]
    subprocess.check_call(cmd)
    return ' '.join(cmd)


def update_rpath(g_dest='lib/amber_3rd_party/', copy_gfortran=True):
    # current folder
    will_be_fixed = get_will_be_fixed_files()
    gfortran_files = [os.path.join(g_dest, fn) for fn in required_libs]
    all_files = will_be_fixed

    if copy_gfortran:
        all_files = gfortran_files + will_be_fixed

    for fn in all_files:
        for dep in get_dependence(fn):
            change_to_rpath_dot_lib(dep, fn)

    # update id for gfortran related files
    if copy_gfortran:
        for fn in gfortran_files:
            basename = os.path.basename(fn)
            cmd_id = [
                'install_name_tool', '-id',
                '@rpath/amber_3rd_party/{}'.format(basename), fn
            ]
            subprocess.check_call(cmd_id)

    for fn in will_be_fixed:
        # we will store all gfortran-relates files in
        # $AMBERHOME/lib/amber_3rd_party
        if fn.endswith('.dylib'):
            add_rpath(fn, '@loader_path/amber_3rd_party')
        else:
            try:
                add_rpath(fn, '@loader_path/../lib/amber_3rd_party')
            except RuntimeError as e:
                print('WARNING add_rpath failed for {}'.format(fn))


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy-gfortran", action="store_true")
    opt = parser.parse_args(args)
    dest = 'lib/amber_3rd_party'
    try:
        os.makedirs(dest)
    except OSError:
        pass
    if opt.copy_gfortran:
        copy_gfortran_libs(
            g_dir='/usr/local/gfortran/lib', dest='lib/amber_3rd_party/')
    update_rpath(copy_gfortran=opt.copy_gfortran)


if __name__ == '__main__':
    main()
