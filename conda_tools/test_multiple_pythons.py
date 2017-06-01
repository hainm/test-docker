import os
import sys
import subprocess
from contextlib import contextmanager

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


def main():
    package_dir = sys.argv[1]
    conda_recipe = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'conda-recipe'))
    run_test = '{}/run_test.sh'.format(conda_recipe)
    print('conda_recipe', conda_recipe)
    print('run_test', run_test)

    for py in ['2.7', '3.4', '3.5', '3.6']:
        env_name = ENV_ROOT + py
        with run_env(env_name, py):
            subprocess.check_call(
                'conda install {} -n {}'.format(package_dir, env_name),
                shell=True)
            subprocess.check_call('bash {}'.format(run_test), shell=True)


if __name__ == '__main__':
    main()
