import os
import itertools
import subprocess
import itertools
import argparse

DRY_RUN = False

def is_object_file(fn):
    return os.path.isfile(fn) and 'is not an object file' not in subprocess.check_output([
        'otool', '-L', fn]).decode()

def easy_check_output(cmd):
    try:
        return subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        print("FAIL to run command", " ".join(cmd))

def add_loader_path(fn, prefix, sub):
    """Add loader_path for `fn` to `prefix`
    """
    relpath = os.path.relpath(prefix, os.path.abspath(os.path.dirname(fn)))
    loader_path = '@loader_path/{}/{}'.format(relpath, sub)
    if not loader_path in subprocess.check_output(['otool', '-l', fn]).decode():
        cmd = ['install_name_tool', '-add_rpath', loader_path, fn]
        if DRY_RUN:
            print(cmd)
        else:
            easy_check_output(cmd)
    else:
        print("{} is already in {}".format(loader_path, fn))


def add_id(fn):
    """Change absolute path to @rpath/{basename}
    """
    basename = os.path.basename(fn)
    cmd = ['install_name_tool', '-id',
         '@rpath/%s' % basename, fn]
    if DRY_RUN:
        print(cmd)
    else:
        subprocess.check_call(cmd)


def get_file_object_from_prefix(pkg_name):
    """return generator
    """
    pkg_dir = os.path.abspath(pkg_name)
    bin_iter = os.walk(os.path.join(pkg_name, 'bin'))
    lib_iter = os.walk(os.path.join(pkg_name, 'lib'))
    for root, dirs, files in itertools.chain(bin_iter, lib_iter):
        for fn in (os.path.join(root, _) for _ in files):
            if not fn.endswith('.a') and is_object_file(fn):
            # if fn.endswith('.so') or fn.endswith('.dylib'):
                yield fn


def fix_linking_libs(fn, lib_paths, prefix=None):
    # change to @rpath instead of using absolute path
    lib_paths = lib_paths if prefix is None else [
            lib for lib in lib_paths if lib.startswith(prefix)]
    for lib_path in lib_paths:
        basename = os.path.basename(lib_path)
        cmd = [
            'install_name_tool', '-change', lib_path,
            '@rpath/{}'.format(basename), fn
        ]
        if DRY_RUN:
            print(cmd)
        else:
            subprocess.check_call(cmd)


def get_dylibs(fn):
    basename = os.path.basename(fn)
    output = subprocess.check_output(['otool', '-L', fn]).decode()
    lines = [line.split()[0] for line in output.split('\n') if line
            and basename not in line]
    return lines


def handle_gfortran_libs(pkg_name):
    pass


def main(args=None):
    global DRY_RUN
    parser = argparse.ArgumentParser(description="Fix rpath and loader_path for files in "
        "path/{bin,lib} folders")
    parser.add_argument('path')
    parser.add_argument('--prefix', help='prefix got from running otool -L')
    parser.add_argument('-d', '--dry-run', action='store_true')
    opt = parser.parse_args(args)

    if opt.dry_run:
        DRY_RUN = True

    if opt.prefix is None:
        opt.prefix = os.path.abspath(opt.path)

    pkg_name = os.path.abspath(opt.path)
    for fn in get_file_object_from_prefix(pkg_name):
        add_id(fn)
        add_loader_path(fn, pkg_name, 'lib')
        libs = get_dylibs(fn)
        fix_linking_libs(fn, libs, prefix=opt.prefix)
    handle_gfortran_libs(pkg_name)


if __name__ == '__main__':
    main()
