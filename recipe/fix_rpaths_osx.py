import os
from glob import glob
import subprocess

def get_dylibs(fn):
    try:
        output = subprocess.check_output([
            'otool',
            '-L',
            fn
        ]).decode()
        return [line.split()[0] for line in output.split('\n') if line][2:]
    except subprocess.CalledProcessError:
        return []

def update_id(lib_path):
    basename = os.path.basename(lib_path)
    subprocess.check_call(
        'install_name_tool -id @rpath/{} {}'.format(basename, lib_path),
        shell=True)

def fix_linking_libs(target, lib_paths):
    for lib_path in lib_paths:
        basename = os.path.basename(lib_path)
        subprocess.check_call(['install_name_tool', '-change', 
                               lib_path,
                               '@rpath/{}'.format(basename),
                               target])
def get_needed_to_be_fixed_libs():
    need_tobe_fixed_libs = []
    for lib in glob('*.dylib'):
        for linked_lib in get_dylibs(lib):
            if 'conda' in linked_lib:
                need_tobe_fixed_libs.append(linked_lib)
                break


if __name__ == '__main__':
    for target in glob('tmp/*'):
        lib_paths = [lib_path for lib_path in get_dylibs(target) if 'conda' in lib_path]
        if target.endswith('dylib'):
            update_id(target)
        fix_linking_libs(target, lib_paths)

        # test
        subprocess.call('otool -L {}'.format(target), shell=True)
