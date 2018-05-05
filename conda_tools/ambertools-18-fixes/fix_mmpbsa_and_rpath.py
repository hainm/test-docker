import os
import sys
sys.path.append('/Users/haichit/amber_git/ambertools-binary-build/conda_tools')

import edit_package
import subprocess

cmd = ['python', '/Users/haichit/amber_git/ambertools-binary-build/conda_tools/fix_rpath_osx.py']
with  edit_package.editing_conda_package('../amber-conda-bld/osx-64/ambertools-18.0-0.tar.bz2', add_date=False, conda=True):
    cmd2 = cmd + [os.getcwd()]
    subprocess.call(cmd2)
    subprocess.call(['2to3', '-w', 'bin/MMPBSA.py'])
    subprocess.call(['rm', 'bin/MMPBSA.py.bak'])
