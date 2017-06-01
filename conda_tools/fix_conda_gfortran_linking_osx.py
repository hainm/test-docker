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

import argparse

# local file, in the same folder as this script
from edit_package import editing_conda_package
import update_gfortran_libs_osx


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('tarfile', nargs='?', help='targer file')
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default='conda/osx-64',
        help="output directory")
    parser.add_argument("-d", "--dry_run", action="store_true", help="dry run")
    opt = parser.parse_args(args)
    repack_conda_package(opt)


def repack_conda_package(opt):
    with editing_conda_package(
            opt.tarfile,
            output_dir=opt.output_dir,
            add_date=False,
            dry_run=opt.dry_run,
            conda=True):
        # we do not include libgfortran here
        # will add amber-libgfortran requirement in meta file?
        update_gfortran_libs_osx.main([])


if __name__ == '__main__':
    main()
