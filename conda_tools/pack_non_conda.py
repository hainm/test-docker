# Aim: Mostly for phenix users and those don't like using Miniconda

# 1. wget url_to_tar_file.tar
# 2. tar -xf url_to_tar_file.tar
# 3. source amber17/ambersh
# 4. Just it
""" Usage example: python pack_binary_without_conda_install.py ambertools-17.0.1-py27_1.tar.bz2

Note: You can use file pattern

This script will unpack that bz2 file, then do some editing, then pack it to ./non-conda-install folder.
This should be done after doing conda-build
"""

import os
import subprocess
from glob import glob
import argparse

# local file, in the same folder as this script
from edit_package import editing_conda_package


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tarfile', nargs='?', help='targer file')
    parser.add_argument(
        "--output-dir",
        type=str,
        default='./non-conda-install',
        dest="output_dir",
        help="output directory")
    parser.add_argument(
        "--date", action="store_true", help="Add date to output tarfile")
    parser.add_argument("-d", "--dry_run", action="store_true", help="dry run")
    opt = parser.parse_args()
    pack_non_conda_package(opt)


def pack_non_conda_package(opt):
    with editing_conda_package(
            opt.tarfile,
            output_dir=opt.output_dir,
            add_date=opt.date,
            dry_run=opt.dry_run):
        update_python_env('./bin/')

        # No need to copy here since we alread done in conda build step?


def update_python_env(bin_dir):
    files = [fn for fn in glob(bin_dir + '/*') if os.path.isfile(fn)]
    for fn in files:
        try:
            content = ''
            with open(fn) as fh:
                line = fh.readline().strip()
                if 'bin/python' in line:
                    fh.seek(0)
                    content = fh.read().replace(line, '#!/usr/bin/env python')
            # overwrite
            if content:
                with open(fn, 'w') as fh:
                    fh.write(content)
                subprocess.check_call(['chmod', '+x', fn])
        except UnicodeError:
            pass


if __name__ == '__main__':
    main()
