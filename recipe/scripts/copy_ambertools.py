#!/usr/bin/env python
import os
import subprocess

def mkdir_ambertree():
    for folder in ['dat', 'doc', 'AmberTools', 'AmberTools/src', 'AmberTools/test']:
        try:
            os.mkdir(folder)
        except OSError:
            pass

def copy_tree():
    # use mkrelease_at as a file source
    recipe_dir = os.getenv('RECIPE_DIR', 'AmberTools/src/conda-recipe')
    amberhome = os.path.join(recipe_dir, '..', '..', '..')
    mkrelease_at_file = os.path.join(amberhome, 'mkrelease_at')
    extra_folders = ['nfe-umbrella-slice']
    extra_dirs = [os.path.join(amberhome, 'AmberTools', 'src', folder) for folder in extra_folders]
    
    for source_dir in extra_dirs:
        target_dir = os.path.join('AmberTools', 'src')
        print('copying {} to {}'.format(source_dir, target_dir))
        subprocess.call(['cp', '-r', source_dir, target_dir])
    
    with open(mkrelease_at_file) as fh:
        for line in fh.readlines():
            line = line.strip()
            if line.startswith('$TAR'):
                folder_or_folders = line.split('/')[-1]
                if '{' in folder_or_folders:
                    # list of folders
                    # {x,y,z}
                    folders = folder_or_folders.replace('{', '').replace('}', '').split(',')
                else:
                    # single folder
                    folders = [folder_or_folders, ]
                root_dir = '/'.join(line.split('/')[1:-1])

                for folder in folders:
                    if not root_dir:
                        source_dir = os.path.join(amberhome, folder)
                        target_dir = '.'
                    else:
                        source_dir = os.path.join(amberhome, root_dir, folder)
                        target_dir = root_dir
                    print('copying {} to {}'.format(source_dir, target_dir))
                    subprocess.call(['cp', '-r', source_dir, target_dir])

if __name__ == '__main__':
    mkdir_ambertree()
    copy_tree()
