import os
import sys
import shutil
from glob import iglob

import utils


def force_mkdir(src):
    try:
        os.mkdir(src)
    except OSError:
        pass


def copytree_here(src, dest):
    pattern = src + '/*'
    for fn in iglob(pattern):
        cmd = 'cp -rf {} {}'.format(fn, dest)
        print('cmd: ', cmd)
        utils.sh(cmd)


def write_amber_sh(recipe_dir, prefix, pyver):
    with open(os.path.join(recipe_dir, '..', 'conda_tools', 'amber.sh')) as fh, \
            open(os.path.join(prefix, 'amber.sh'), 'w') as fw:
        content = fh.read()
        content = content.replace('pythonX.Y', 'python{}'.format(pyver))
        fw.write(content)
    utils.sh('chmod +x {}/amber.sh'.format(prefix))


def copy_to_prefix(amberhome, prefix):
    recipe_dir = os.getenv('RECIPE_DIR')
    prefix_bin = os.path.join(prefix, 'bin/')
    prefix_lib = os.path.join(prefix, 'lib/')
    prefix_include = os.path.join(prefix, 'include/')
    prefix_dat = os.path.join(prefix, 'dat/')

    force_mkdir(prefix_bin)
    force_mkdir(prefix_lib)
    force_mkdir(prefix_include)
    force_mkdir(prefix_dat)

    # info + license
    readme = os.path.join(amberhome, 'README')
    new_readme = 'README.AmberTools'
    license = os.path.join(amberhome, 'AmberTools', 'LICENSE')
    new_license = 'LICENSE.AmberTools'

    for fn, new_fn in zip([readme, license], [new_readme, new_license]):
        if os.path.exists(fn):
            shutil.copy(fn, os.path.join(prefix, new_fn))
        elif os.path.exists(new_fn):
            shutil.copy(new_fn, prefix)

    amber_python = os.path.join(amberhome, 'bin', 'amber.python')
    try:
        os.remove(amber_python)
    except OSError:
        pass

    # bin
    copytree_here(os.path.join(amberhome, 'bin'), prefix_bin)

    configure_python = os.path.join(amberhome, 'AmberTools', 'src',
                                    'configure_python')
    if os.path.exists(configure_python):
        shutil.copy(configure_python, prefix_bin)

    shutil.copy(
        os.path.join(recipe_dir, '..', 'conda_tools',
                     'amber.setup_test_folders'), prefix_bin)
    shutil.copy(
        os.path.join(recipe_dir, '..', 'conda_tools', 'amber.run_tests'),
        prefix_bin)

    # Lib
    copytree_here(os.path.join(amberhome, 'lib'), prefix_lib)

    # include
    copytree_here(os.path.join(amberhome, 'include'), prefix_include)

    # include
    copytree_here(os.path.join(amberhome, 'dat'), prefix_dat)

    pyver = '.'.join(str(x) for x in sys.version_info[:2])
    write_amber_sh(recipe_dir, prefix, pyver)


if __name__ == '__main__':
    amberhome = '/Users/haichit/amber_git/amber/'
    prefix = './tmp'
    os.environ[
        'RECIPE_DIR'] = '/Users/haichit/amber_git/amber/AmberTools/src/binary-build/conda-recipe'
    copy_to_prefix(amberhome, prefix)
