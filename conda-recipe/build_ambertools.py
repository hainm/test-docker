import os
import sys
from multiprocessing import cpu_count


THIS_RECIPE = os.getenv('RECIPE_DIR', '')
conda_tools_dir = os.path.join(THIS_RECIPE, '..', 'conda_tools')
sys.path.insert(0, conda_tools_dir)
import utils # conda_tools
import copy_ambertools
import fix_rpath_osx
from copy_built_ambertools import copy_to_prefix

def main():
    isosx = sys.platform.startswith('darwin')
    amber_build_task = os.getenv('AMBER_BUILD_TASK', 'ambertools').lower()
    prefix = os.getenv('PREFIX')
    
    if amber_build_task == "ambermini":
        print("Please use conda build $RECIPE_DIR/../conda-ambermini-recipe to avoid Python depedency")
        sys.exit(1)
    
    copy_ambertools.main()
    
    amberhome = os.getcwd()
    os.environ['AMBERHOME'] = amberhome
    utils.set_compiler_env()
    utils.update_amber()
    utils.run_configure()
    
    if amber_build_task == "ambertools":
        utils.sh('make install -j{}'.format(cpu_count()))
    else:
        # e.g: make sander
        if amber_build_task in ['pytraj', 'parmed', 'pymdgx', 'pysander']:
                utils.sh("cd AmberTools/src/ && make {}".format(amber_build_task))
        elif amber_build_task == 'pdb4amber':
                utils.sh("cd AmberTools/src/ && make parmed")
                utils.sh("cd AmberTools/src/ && make pdb4amber")
        elif amber_build_task == 'nab':
                utils.sh("cd AmberTools/src/ && make nabonly")
                utils.sh("cd AmberTools/src/leap && make install")
        else:
            utils.sh("cd AmberTools/src/{} && make".format(amber_build_task))
    
    if isosx:
        # fix rpath
        # $PYTHON ${RECIPE_DIR}/../conda_tools/fix_rpath_osx.py $AMBERHOME/bin/
        # $PYTHON ${RECIPE_DIR}/../conda_tools/fix_rpath_osx.py $AMBERHOME/lib/
        fix_rpath_osx.main([amberhome]) # conda-build seems not help.
    
    copy_to_prefix(amberhome, prefix)


if __name__ == '__main__':
    main()
