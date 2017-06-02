import os
import sys
import subprocess
from contextlib import contextmanager
import argparse
import glob

ENV_ROOT = 'test_ambertools'


def find_miniconda_root():
    command = "conda info | grep 'root environment'"
    output = subprocess.check_output(command, shell=True).decode()
    return output.split()[3] + '/'


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


def ensure_no_gfortran_local(env_name):
    dest = find_miniconda_root() + '/envs/' + env_name

    errors = []

    for fn in get_tested_files(dest):
        cmd = ['otool', '-L', fn]
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.PIPE).decode()
        except subprocess.CalledProcessError:
            output = ''
        if  '/usr/local/gfortran' in output:
            errors.append(fn)

    return errors


def get_so_files(dest):
    cmd = 'find {} -type f -name "*.so"'.format(dest)
    print('cmd: {}'.format(cmd))
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode()
    return [fn for fn in output.split('\n') if fn]


def get_tested_files(dest):
    so_files = get_so_files(dest)
    # files_in_bin = [os.path.join(dest, 'bin', fn)
    #     for fn in ['cpptraj', 'sqm', 'mdgx']]
    files_in_bin = glob.glob(os.path.join(dest, 'bin/*'))
    return [
        fn
        for fn in so_files + files_in_bin
                           + glob.glob(os.path.join(dest, 'bin/to_be_dispatched/*'))
                           + glob.glob(os.path.join(dest, 'lib/*dylib'))
    ]



def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("package_dir")
    parser.add_argument("-py", dest='pyvers')
    opt = parser.parse_args(args)
    package_dir = opt.package_dir

    conda_recipe = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'conda-recipe'))
    run_test = '{}/run_test.sh'.format(conda_recipe)
    print('conda_recipe', conda_recipe)
    print('run_test', run_test)

    pyvers = [opt.pyvers, ] if opt.pyvers else ['2.7', '3.4', '3.5', '3.6']
    print('Python versions = {}'.format(pyvers))

    errors = []
    for py in pyvers:
        env_name = ENV_ROOT + py
        with run_env(env_name, py):
            subprocess.check_call(
                'conda install {} -n {}'.format(package_dir, env_name),
                shell=True)
            if sys.platform.startswith('darwin'):
                errors = ensure_no_gfortran_local(env_name)
            subprocess.check_call('bash {}'.format(run_test), shell=True)
        if errors:
            print("ERROR: Files should not have /usr/local/gfortran in its content")
            print(errors)
            sys.exit(1)


if __name__ == '__main__':
    main()
