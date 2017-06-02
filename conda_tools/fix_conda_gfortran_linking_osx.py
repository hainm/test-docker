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
