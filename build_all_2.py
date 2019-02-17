import os
import sys
import subprocess
import argparse
from glob import glob
from pathlib import Path

sys.path.insert(0,
        str((Path(os.path.dirname(__file__)) / 'conda_tools').absolute()))


def add_path(my_path='/usr/local/gfortran/bin'):
    os.environ['PATH'] = my_path + ':' + os.environ.get('PATH', '')


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "amberhome", help="Path to amber source code")
    parser.add_argument(
        '--output-dir',
        default='.')
    opt = parser.parse_args(args)
    opt.amberhome = os.path.abspath(opt.amberhome)

    if sys.platform.startswith('darwin'):
        # force macos build to use gfortran/gcc/g++
        add_path(my_path='/usr/local/gfortran/bin')
    build(opt)


def build(opt):
    print(sys.path)
    import utils # from conda_tools
    import copy_ambertools

    working_dir = os.path.join(opt.output_dir, 'working_dir')
    try:
        os.mkdir('working_dir')
    except FileExistsError:
        pass
    cwd = os.getcwd()
    os.environ['AMBER_SRC'] = opt.amberhome
    os.environ['AMBERHOME'] = os.path.abspath(working_dir)
    try:
        os.chdir(working_dir)
        copy_ambertools.main()
        utils.update_amber()
        with utils.run_env('py2.7', '2.7'):
            utils.run_configure()
            utils.make_install()
        # for pyver in ['3.4', '3.5', '3.6', '3.7']:
        for pyver in ['3.6', '3.7']:
            with utils.run_env('py%s' % pyver, pyver):
                utils.run_configure()
                utils.make_python_serial()
    finally:
        os.chdir(cwd)


if __name__ == '__main__':
    main()
