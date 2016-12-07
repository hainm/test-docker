import os
import sys
import shutil
import json
from glob import iglob
import subprocess
import tarfile

'''python copy_and_update_conda_package.py /path/to/ambertools*bz2 .

Require: conda
'''

def main():
    bz2_fn = sys.argv[1]
    local_dir = os.path.abspath(sys.argv[2])

    assert os.path.isfile(bz2_fn)
    
    metadata = get_metadata(bz2_fn)
    subdir = metadata['subdir']
    abspath_subdir = os.path.join(local_dir, subdir)
    if not os.path.exists(abspath_subdir):
        os.mkdir(abspath_subdir)
    shutil.copy(bz2_fn, abspath_subdir)
    subprocess.check_call(['conda', 'index', abspath_subdir])

def get_metadata(fn):
    # get index.json from tarfile
    # mostly for detecting built platform to create correct folder
    # e.g: tar.bz file was built in osx will be copied to osx-64 folder
    with tarfile.open(fn) as fh:
        with fh.extractfile('info/index.json') as info_fh:
            content = info_fh.read().decode()
            package_dict = json.loads(content)
    return package_dict


if __name__ == '__main__':
    # fn = '../ambermini101-16.20-py35_1.tar.bz2'
    # print(get_metadata(fn))
    main()
