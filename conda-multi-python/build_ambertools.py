#!/bin/sh
import os
import sys
from glob import glob
import shutil

THIS_RECIPE = os.getenv('RECIPE_DIR', '')
conda_tools_dir = os.path.join(THIS_RECIPE, '..', 'conda_tools')
print('conda_tools_dir', conda_tools_dir)
sys.path.insert(0, conda_tools_dir)
import utils # conda_tools
import copy_ambertools


def main():
    PREFIX = os.getenv('PREFIX')
    AMBERHOME = os.getcwd()
    os.environ['AMBERHOME'] = AMBERHOME

    copy_ambertools.main()
    ATPY2 = utils.get_package_dir(
        conda_recipe=os.path.join(THIS_RECIPE, '..', 'conda-recipe'), py=2.7)
    utils.tar_xf(ATPY2)

    utils.update_amber()
    utils.set_compiler_env()
    utils.run_configure()

    os.chdir('AmberTools/src')
    utils.make_python_serial()
    os.chdir(AMBERHOME)

    python_ver = ".".join(map(str, sys.version_info[:2]))
    prefix_bin = os.path.join(PREFIX, 'bin')
    shutil.copy('{}/bin/pdb4amber'.format(AMBERHOME), prefix_bin)
    shutil.copy('{}/bin/parmed'.format(AMBERHOME), prefix_bin)

    for fn in glob('{}/lib/*'.format(AMBERHOME)):
        # only need some libraries for pytraj/libcpptraj
        if os.path.isfile(fn):
            shutil.copy(fn, '{}/lib/'.format(PREFIX))

    utils.sh('cp -rf {}/lib/python{} {}/lib/'.format(AMBERHOME, python_ver, PREFIX))
    shutil.rmtree('./info')


if __name__ == '__main__':
    main()
