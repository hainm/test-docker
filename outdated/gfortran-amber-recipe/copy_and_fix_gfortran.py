'''This script will
- copy gfortran-related to lib/amber_3rd_party folder and fix the rpath
- Link lib/*.dylib and bin/{cpptraj, mdgx, ...} to that lib/amber_3rd_party folder
'''

import os
import shutil
import glob
import subprocess
from conda_build.os_utils import macho


required_libs = [
    'libstdc++.6.dylib', 'libgfortran.3.dylib', 'libgcc_s.1.dylib',
    'libquadmath.0.dylib'
]


# assume you are in $AMBERHOME
def get_will_be_fixed_files():
    so_files = get_so_files()
    return [
        fn
        for fn in so_files + glob.glob('bin/*')
                 + glob.glob('bin/to_be_dispatched/*')
                 + glob.glob('lib/*dylib')
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
        print('orig_lib', orig_lib)
        return [
            lib for lib in macho.get_dylibs(orig_lib)
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


def update_rpath(g_dest='lib/amber_3rd_party/'):
    # current folder
    will_be_fixed = get_will_be_fixed_files()
    all_files = [g_dest + fn for fn in required_libs] + will_be_fixed
    for fn in all_files:
        for dep in get_dependence(fn):
            change_to_rpath_dot_lib(dep, fn)
        
        # update id
        basename = os.path.basename(fn)
        cmd = ['install_name_tool', '-id', '@rpath/amber_3rd_party/{}'.format(basename),
               fn]

        subprocess.check_call(cmd)

    for fn in will_be_fixed:
        # we will store all gfortran-relates files in
        # $AMBERHOME/lib/amber_3rd_party
        if fn.endswith('.dylib'):
            macho.add_rpath(fn, '@loader_path/amber_3rd_party')
        else:
            macho.add_rpath(fn, '@loader_path/../lib/amber_3rd_party')


def main():
    dest = 'lib/amber_3rd_party'
    try:
        os.makedirs(dest)
    except OSError:
        pass
    copy_gfortran_libs(g_dir='/usr/local/gfortran/lib', dest='lib/amber_3rd_party/')
    update_rpath()


if __name__ == '__main__':
    main()
