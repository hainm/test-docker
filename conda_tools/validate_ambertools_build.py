import os
import sys
import subprocess
from contextlib import contextmanager
import argparse
import glob

ENV_ROOT = 'test_ambertools'
AMBER_VERSION = 'amber17'


def is_conda_package(package_dir):
    basename = os.path.basename(package_dir)
    return not (basename.startswith('osx') or basename.startswith('linux'))


def run_test(package_dir, amberhome, TEST_SCRIPT):
    if is_conda_package(package_dir):
        subprocess.check_call('bash {}'.format(TEST_SCRIPT), shell=True)
    else:
        subprocess.check_call(
            "source {}/amber.sh && bash {}".format(amberhome, TEST_SCRIPT),
            shell=True)


def install_ambertools(package_dir,
                       env_name,
                       tmp_dir='junk_folder',
                       pyver='2.7'):
    if is_conda_package(package_dir):
        # conda
        subprocess.check_call(
            'conda install {} -n {}'.format(package_dir, env_name), shell=True)
    else:
        amberhome = os.path.abspath(os.path.join(tmp_dir, AMBER_VERSION))
        # non-conda
        try:
            os.mkdir(tmp_dir)
        except OSError:
            pass
        os.chdir(tmp_dir)
        if os.path.exists(AMBER_VERSION):
            print("Existing {}. Skip untar".format(AMBER_VERSION))
        else:
            subprocess.check_call(['tar', '-xf', package_dir])
        # os.environ['AMBERHOME'] = amberhome
        # os.environ['PYTHONPATH'] = os.path.join(amberhome,
        #         'lib/python{}/site-packages'.format(pyver))
        # os.environ['PATH'] = os.path.join(amberhome, 'bin') + ':' + os.getenv("PATH")


def find_miniconda_root():
    command = "conda info --base"
    return subprocess.check_output(command, shell=True).decode().strip()


def create_env(env, python_version):
    sys.stdout.write('creating {} env'.format(env))
    cmlist = 'conda create -n {} python={} numpy nomkl --yes'.format(
        env, python_version)
    print(cmlist)
    subprocess.check_call(cmlist.split())


@contextmanager
def run_env(env_name, python_version):
    os.environ['PYTHONPATH'] = ''
    ORIG_PATH = os.environ['PATH']
    env_path = find_miniconda_root() + '/envs/' + env_name
    env_bin_dir = env_path + '/bin/'
    os.environ['CONDA_PREFIX'] = env_path
    os.environ['PATH'] = env_bin_dir + ':' + ORIG_PATH

    if not os.path.exists(find_miniconda_root() + '/envs/' + env_name):
        create_env(env_name, python_version)
    os.system('source activate {}'.format(env_name))

    yield

    os.system('conda env remove -n {} -y'.format(env_name))
    os.environ['PATH'] = ORIG_PATH


def ensure_no_gfortran_local(amberhome):
    errors = []

    for fn in get_tested_files(amberhome):
        cmd = ['otool', '-L', fn]
        try:
            output = subprocess.check_output(
                cmd, stderr=subprocess.PIPE).decode()
        except subprocess.CalledProcessError:
            output = ''
        if '/usr/local/gfortran' in output:
            errors.append(fn)

    return errors


def get_so_files(dest):
    cmd = 'find {} -type f -name "*.so"'.format(dest)
    print('cmd: {}'.format(cmd))
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode()
    files = [fn for fn in output.split('\n') if fn]
    return files


def get_tested_files(dest):
    so_files = get_so_files(dest)
    # files_in_bin = [os.path.join(dest, 'bin', fn)
    #     for fn in ['cpptraj', 'sqm', 'mdgx']]
    files_in_bin = glob.glob(os.path.join(dest, 'bin/*'))
    return [
        fn
        for fn in so_files + files_in_bin + glob.glob(
            os.path.join(dest, 'bin/to_be_dispatched/*')) + glob.glob(
                os.path.join(dest, 'lib/*dylib'))
    ]


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("package_dir")
    parser.add_argument("-py", dest='pyvers')
    opt = parser.parse_args(args)
    package_dir = opt.package_dir
    tmp_dir = 'junk_folder'  # only exists if non-conda package

    conda_recipe = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'conda-ambertools-single-python'))
    TEST_SCRIPT = '{}/run_test.sh'.format(conda_recipe)
    print('conda_recipe', conda_recipe)
    print('run_test', run_test)

    pyvers = [
        opt.pyvers,
    ] if opt.pyvers else ['2.7', '3.4', '3.5', '3.6', '3.7']
    print('Python versions = {}'.format(pyvers))
    print('conda package = {}'.format(is_conda_package(package_dir)))

    errors = []
    for py in pyvers:
        env_name = ENV_ROOT + py
        with run_env(env_name, py):
            if is_conda_package(package_dir):
                amberhome = find_miniconda_root() + '/envs/' + env_name
            else:
                # do not set CONDA_PREFIX to trigger
                # unset PYTHONPATH in run_test.sh in this case.
                os.environ['CONDA_PREFIX'] = ''
                amberhome = os.path.join(
                    os.path.abspath(tmp_dir), AMBER_VERSION)

            install_ambertools(package_dir, env_name, pyver=py)
            if sys.platform.startswith('darwin'):
                errors = ensure_no_gfortran_local(amberhome)

            run_test(package_dir, amberhome, TEST_SCRIPT)

        # check libgfortran
        if errors:
            print(
                "ERROR: Files should not have /usr/local/gfortran in its content"
            )
            print(errors)
            sys.exit(1)
        else:
            print("libgfortran fixed. Wonderful")


if __name__ == '__main__':
    main()
