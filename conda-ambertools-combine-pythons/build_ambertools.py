#!/bin/sh

# overwrite amber.sh
import os
import sys
import shutil
from glob import glob
sys.path.insert(0, '../conda_tools')

THIS_RECIPE = os.getenv('RECIPE_DIR', '')
conda_tools_dir = os.path.join(THIS_RECIPE, '..', 'conda_tools')
print('conda_tools_dir', conda_tools_dir)
sys.path.insert(0, conda_tools_dir)
import utils # conda_tools
from copy_built_ambertools import copy_to_prefix
import update_gfortran_libs_osx


def main():
    amberhome = os.getcwd()
    os.environ['AMBERHOME'] = amberhome
    
    THIS_RECIPE = os.getenv('RECIPE_DIR')
    PREFIX = os.getenv('PREFIX')
    ATPY2 = utils.get_package_dir(conda_recipe=os.path.join(THIS_RECIPE, '..', 'conda-ambertools-single-python'),
            py=2.7)
    at_temp_folder = os.path.dirname(ATPY2)
    
    utils.tar_xf(ATPY2)
    shutil.rmtree('./info')
    
    at_tempfile=os.path.join(at_temp_folder,
            'ambertools_tempfile*.tar.bz2')
    
    for fn in glob(at_tempfile):
        utils.sh("tar -xf {}".format(fn))
        shutil.rmtree("./info")
    
    copy_to_prefix(amberhome, PREFIX)
    shutil.copy(os.path.join(THIS_RECIPE, '..', 'conda_tools', 'amber_all_pythons.sh'),
            os.path.join(PREFIX, 'amber.sh'))
    
    if sys.platform.startswith("darwin"):
        update_gfortran_libs_osx.main([PREFIX, '--copy-gfortran'])
       

if __name__ == '__main__':
    main()
