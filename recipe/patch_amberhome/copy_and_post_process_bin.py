#!/usr/bin/env python

import os
from glob import glob
import subprocess
from itertools import chain

template = """
#!/usr/bin/env python

import os
import sys
import subprocess

os.environ['AMBERHOME'] = sys.prefix
{exe}_exe = os.path.join(sys.prefix, 'bin', '_{exe}')
try:
    subprocess.call(commands)
except KeyboardInterrupt:
    pass
"""

def post_exe_for_prefix_folder(exe_path):
    # always assuming having PREFIX env
    prefix_bin = os.getenv('PREFIX', '') + '/bin/'
    basename = os.path.basename(exe_path)
    subprocess.check_call(['cp', exe_path, prefix_bin + '_' +  basename])
    with open(prefix_bin + basename, 'w') as fh:
        fh.write(template.format(exe=basename))

def get_all_exe_paths_requiring_amberhome():
    amberhome = os.getenv('AMBERHOME', '')
    amber_bin = amberhome + '/bin/'

    all_exe = []
    for exe in glob(amber_bin + '*'):
        try:
            output = subprocess.check_output(['grep', 'AMBERHOME', exe]).decode()
        except subprocess.CalledProcessError:
            pass
        all_exe.extend([line.split()[2]
                       for line in output.split('\n') if 'matches' in line])
    return set(all_exe)
    
def main():
    for exe_path in get_all_exe_paths_requiring_amberhome():
        print(template.format(exe=os.path.basename(exe_path)))
        # post_exe_for_prefix_folder(exe_path)

if __name__ == '__main__':
    main()
