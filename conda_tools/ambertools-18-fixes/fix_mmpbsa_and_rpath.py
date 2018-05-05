import os
import sys

ambertools_tar = sys.argv[1]

conda_tools_path = os.path.join(os.path.dirname(__file__), '..', 'conda_tools')

sys.path.append(conda_tools_path)

import edit_package
import subprocess

cmd = ['python', f'{conda_tools}/fix_rpath_osx.py']
with  edit_package.editing_conda_package(ambertools_tar, add_date=False, conda=True):
    cmd2 = cmd + [os.getcwd()]
    subprocess.call(cmd2)
    subprocess.call(['2to3', '-w', 'bin/MMPBSA.py'])
    subprocess.call(['rm', 'bin/MMPBSA.py.bak'])
