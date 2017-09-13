# WARNING: Your current working dir must be outside amber tree.
# See usage below
''' Building AmberTools binary for conda and non-conda install
for python 2.7, 3.4, 3.5, 3.6 for Linux and MacOS

Require: MacOS + docker + Python stuff + two cups of coffee.

How to run?

    mkdir $HOME/TMP # or any name/dir you want
    cd $HOME/TMP
    python /path/to/AMBERHOME/AmberTools/src/conda_tools/build_all.py

    # use -h or --help for further usage

Expectation

This script will create a folder tree (below) in current folder:

    amber-conda-bld:
        linux-64
        osx-64
'''
import os
import sys
import subprocess
import argparse
from glob import glob


CONTAINER_FOLDER = 'amber-conda-bld'
AMBER_BINARY_BUILD_DIR = os.path.abspath(os.path.dirname(__file__))
CONDA_TOOLS_DIR = os.path.join(AMBER_BINARY_BUILD_DIR, 'conda_tools')
DOCKER_BUILD_SCRIPT = os.path.join(
    AMBER_BINARY_BUILD_DIR,
    'conda-recipe/scripts/run_docker_build.sh'
)
BZ2_FILES = []


def write_meta_file(amber_ver):
    # assume amber_ver is this format 17.4
    version, bugfix = amber_ver.split('.')
    recipe_dir = os.path.join(os.path.dirname(__file__),
            'conda-ambertools-all-python')
    with open(os.path.join(recipe_dir, 'meta.template')) as fh, \
         open(os.path.join(recipe_dir, 'meta.yaml'), 'w') as fh_new:
         content = fh.read()
         content = content.replace('{% set version = "0" %}',
                                   '{{% set version = "{}" %}}'.format(version))
         content = content.replace('{% set bugfix_version = "0" %}',
                                   '{{% set bugfix_version = "{}" %}}'.format(bugfix))
         fh_new.write(content)

def assert_amber_src_exists(amberhome):
    if not os.path.exists(amberhome+ '/AmberTools'):
        print("AmberTools does not exist in {}".format(amberhome))
        sys.exit(1)


def built_tarfile_dir(build_commands):
    built_file = subprocess.check_output(build_commands + ['--output'
                                                           ]).decode().strip()
    return built_file


def sh(command):
    subprocess.check_call(command, shell=True)


def add_path(my_path='/usr/local/gfortran/bin'):
    os.environ['PATH'] = my_path + ':' + os.environ.get('PATH', '')


def copy_tarfile_to_build_folder(build_commands,
                                 container_folder,
                                 dry_run=False):
    built_file = built_tarfile_dir(build_commands)

    copy_comands = ['cp', built_file, container_folder]
    if dry_run:
        print(copy_comands)
    else:
        subprocess.check_call(copy_comands)
    BZ2_FILES.append(
        os.path.join(container_folder, os.path.basename(built_file)))


def build_all_python_verions_in_one_package(container_folder, dry_run=False,
        py_versions=['3.4', '3.5', '3.6']):
    # build full AmberTools for python 2.7 first
    print("Start with python 2.7. Additional versions", py_versions)
    os.environ['AMBER_BUILD_TASK'] = 'ambertools'
    recipe_dir = os.path.abspath(os.path.join(AMBER_BINARY_BUILD_DIR, 'conda-recipe'))
    tmp_recipe_dir = os.path.abspath(
        os.path.join(AMBER_BINARY_BUILD_DIR, 'conda-multi-python'))
    py2_build_command = ['conda', 'build', recipe_dir, '--py', '2.7']
    if dry_run:
        print(py2_build_command)
    else:
        subprocess.check_call(py2_build_command)

    # build only python packages in AmberTools
    for pyver in py_versions:
        print('pyver', pyver)
        build_command = ['conda', 'build', tmp_recipe_dir, '--py', pyver]
        if dry_run:
            print(build_command)
        else:
            subprocess.check_call(build_command)
        tarfile = built_tarfile_dir(build_command)
        os.environ['AT_TEMP_FILE_FOLDER'] = os.path.dirname(tarfile)

    # build all
    # copy all python packages for different python versions to
    # original full AmberTools build (with python 2.7)
    recipe_dir = tmp_recipe_dir + '/../conda-ambertools-all-python'
    combine_command = ['conda', 'build', recipe_dir]
    if dry_run:
        print(combine_command)
    else:
        subprocess.check_call(combine_command)
        # sh('cp {} .'.format(built_tarfile_dir(combine_command)))
    copy_tarfile_to_build_folder(
        combine_command, container_folder, dry_run=dry_run)


def perform_build_with_docker(opt, container_folder, py_versions=[
        '2.7',
]):
    build_task = opt.build_task
    if opt.build_task == 'ambertools_pack_all_pythons':
        final_python_versions = [
            '2.7'
        ]
        print("Ignoring {}".format(str(py_versions)))
    else:
        final_python_versions = py_versions

    all_tarfiles = []
    for ver in final_python_versions:
        # find AT file path in docker run
        docker_command_build = [
            'bash',
            DOCKER_BUILD_SCRIPT,
            build_task,
            ver,
            opt.amberhome,
            AMBER_BINARY_BUILD_DIR,
            opt.ambertools_version,
        ]
        print('docker_command_build')
        print(" ".join(docker_command_build))

        # dry run to immediately getting output.

        output = subprocess.check_output(docker_command_build + [
            'True',
        ]).decode()
        # find package name from output generated from docker build.
        line_having_AT = [
            line for line in output.split('\n')
            if "['cp', '/root/miniconda3/conda-bld/linux-64/" in line
        ][0]
        tarfile = os.path.basename(
            line_having_AT.split(',')[1].replace("'", ''))
        all_tarfiles.append(tarfile)

        if not opt.dry_run:
            subprocess.check_call(docker_command_build + [
                'False',
            ])
        else:
            print(docker_command_build + ['True'])
            print(output)

    for tarfile in all_tarfiles:
        abspath_tarfile = os.path.join(opt.amberhome, 'linux-64', tarfile)

        move_command = ['mv', abspath_tarfile, container_folder]
        if opt.sudo:
            move_command.insert(0, 'sudo')
        BZ2_FILES.append(os.path.join(container_folder, tarfile))
        if opt.dry_run:
            print(move_command)
        else:
            subprocess.check_call(move_command)


def perform_build_without_docker(opt,
                                 recipe_dir,
                                 container_folder,
                                 py_versions=[
                                     '2.7',
                                 ]):

    if opt.build_task != 'ambermini':
        if opt.build_task == 'ambertools_pack_all_pythons':
            print('Build a single AmberTools with different Python versions')
            final_version = py_versions[:]
            try:
                # we will build py2.7 seperately
                final_version.remove('2.7')
            except ValueError:
                pass
            build_all_python_verions_in_one_package(
                container_folder=container_folder, dry_run=opt.dry_run,
                py_versions=final_version)
        else:
            for ver in py_versions:
                build_commands = ['conda', 'build', recipe_dir, '--py', ver]
                if opt.dry_run:
                    print(build_commands)
                else:
                    subprocess.call(build_commands)
                copy_tarfile_to_build_folder(
                    build_commands, container_folder, dry_run=opt.dry_run)
    else:
        # build ambermini, don't require python
        print("Building ambermini, ignore {}".format(py_versions))
        amber_mini_recipe_dir = recipe_dir + '/../conda-ambermini-recipe'
        build_commands = ['conda', 'build', amber_mini_recipe_dir]
        if opt.dry_run:
            print(build_commands)
        else:
            subprocess.call(build_commands)
        copy_tarfile_to_build_folder(
            build_commands, container_folder, dry_run=opt.dry_run)


def main(args=None):
    global CONTAINER_FOLDER, DOCKER_BUILD_SCRIPT, BZ2_FILES
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--exclude-linux",
        action='store_true',
        dest="exclude_linux",
        help="no Linux build")
    parser.add_argument(
        "--exclude-osx",
        action='store_true',
        dest="exclude_osx",
        help="No OSX build")
    parser.add_argument(
        "--exclude-non-conda-user",
        action='store_true',
        dest="exclude_non_conda_user",
        help="Exclude build for non-conda-user")
    parser.add_argument(
        "--post-processing-all",
        action='store_true',
        dest="post_processing_all",
        help="Post processing all found packages for non-conda install")
    parser.add_argument(
        "-t",
        "--task",
        type=str,
        default='ambertools',
        dest="build_task",
        help="which target you want to build? (default ambertools?)")
    parser.add_argument(
        '-d', "--dry-run", action='store_true', dest="dry_run", help="dry run")
    parser.add_argument(
        "--amberhome", help="Path to amber source code")
    parser.add_argument(
        '--py',
        '--py-version',
        default=None,
        help=
        'Python version. Default: build all versions (2.7, 3.4, 3.5, 3.6)')
    parser.add_argument(
        '-v',
        '--ambertools-version',
        help=
        'AmberTools version, must be something like 17.4',
        required=True)
    parser.add_argument(
        '--no-docker',
        action='store_true',
        dest="no_docker",
        help=
        'Not using docker for building Linux target. This is only for testing, otherwise you must use centos5'
    )
    parser.add_argument(
        '--date',
        action='store_true',
        help=
        'If given, add date to non-conda package (mostly for phenix intergration)'
    )
    parser.add_argument(
        '--sudo',
        action='store_true',
        help='use sudo to move files. Note: for circleci')
    opt = parser.parse_args(args)
    opt.amberhome = os.path.abspath(opt.amberhome)

    if opt.build_task == 'ambertools':
        py_versions = [str(opt.py),] if opt.py else ['2.7', '3.4', '3.5', '3.6']
        opt.build_task = 'ambertools_pack_all_pythons'
    else:
        py_versions = [
            str(opt.py),
        ]

    if sys.platform.startswith('darwin'):
        # force macos build to use gfortran/gcc/g++
        add_path(my_path='/usr/local/gfortran/bin')

    write_meta_file(opt.ambertools_version)

    opt.amberhome = opt.amberhome or os.path.abspath(AMBER_BINARY_BUILD_DIR + '/../../../')
    assert_amber_src_exists(opt.amberhome)

    ORIGINAL_FOLDER = os.getcwd()
    print("Current directory = {}".format(ORIGINAL_FOLDER))
    # store built files
    if not os.path.exists(CONTAINER_FOLDER):
        os.mkdir(CONTAINER_FOLDER)
    CONTAINER_FOLDER = os.path.abspath(CONTAINER_FOLDER)
    container_folder_osx = os.path.join(CONTAINER_FOLDER, 'osx-64')
    if not os.path.exists(container_folder_osx):
        os.mkdir(container_folder_osx)
    container_folder_osx = os.path.abspath(container_folder_osx)
    container_folder_linux = os.path.join(CONTAINER_FOLDER, 'linux-64')
    if not os.path.exists(container_folder_linux):
        os.mkdir(container_folder_linux)
    container_folder_linux = os.path.abspath(container_folder_linux)

    recipe_dir = os.path.join(AMBER_BINARY_BUILD_DIR, 'conda-recipe')
    ambertools_src = os.path.abspath(os.path.join(opt.amberhome, 'AmberTools', 'src'))
    pack_non_conda_package_script = os.path.join(
        CONDA_TOOLS_DIR, 'pack_non_conda.py')

    assert os.path.exists(recipe_dir)
    assert os.path.exists(ambertools_src)
    assert os.path.exists(DOCKER_BUILD_SCRIPT)
    assert os.path.exists(pack_non_conda_package_script)

    build_task = opt.build_task
    print('AMBER_BUILD_TASK = {}'.format(build_task))
    print('AMBERHOME = {}'.format(opt.amberhome))
    print('recipe dir = {}'.format(recipe_dir))

    # go to AmberTools/src
    # We do not got here since conda-build try to remove "dat" folder. ack.
    os.chdir(ambertools_src)
    print('Current working dir = {}'.format(os.getcwd()))

    os.environ['AMBER_BUILD_TASK'] = build_task
    os.environ['AMBER_SRC'] = opt.amberhome

    # OSX build using your MacOS computer
    if not opt.exclude_osx:
        print("Start MacOS build")
        perform_build_without_docker(
            opt,
            recipe_dir=recipe_dir,
            container_folder=container_folder_osx,
            py_versions=py_versions)

    if not opt.exclude_linux:
        if opt.no_docker:
            perform_build_without_docker(
                opt,
                recipe_dir=recipe_dir,
                container_folder=container_folder_linux,
                py_versions=py_versions)
        else:
            print("Linux build via docker container")
            os.chdir(opt.amberhome)
            print('Current working dir = {}'.format(os.getcwd()))

            # ambermini do not require python but still need to pass here
            # since run_docker_build.sh require 2nd argument
            # TODO: remove that
            final_verions = [
                '2.7',
            ] if build_task == 'ambermini' else py_versions
            perform_build_with_docker(
                opt=opt,
                container_folder=container_folder_linux,
                py_versions=final_verions)

    # Post-process conda-built packages for non-conda users
    if not opt.exclude_non_conda_user:
        print("Post processing conda packages for non-conda user")
        os.chdir(CONTAINER_FOLDER)

        bz2_files = []
        if opt.post_processing_all:
            bz2_files = glob('linux-64/*bz2') + glob('osx-64/*bz2')
        else:
            bz2_files = BZ2_FILES

        print('BZ2_FILES', bz2_files)
        final_files = bz2_files[:]
        for fn in bz2_files:
            command_pack = ['python', pack_non_conda_package_script, fn]
            if opt.date:
                command_pack.append('--date')

            command_pack_dry_run = command_pack + ['-d']

            out_fn = [
                line.split()[-1]
                for line in (subprocess.check_output(command_pack_dry_run)
                             .decode().split('\n'))
                if 'ABSOLUTE FILENAME DIR' in line
            ].pop()

            final_files.append(out_fn)
            print(command_pack)
            if not opt.dry_run:
                subprocess.check_call(command_pack)

        print("FINAL")
        for fn in final_files:
            print(fn)


if __name__ == '__main__':
    main()
