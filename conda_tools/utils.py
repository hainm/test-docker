import os
import sys
import subprocess
from contextlib import contextmanager


def get_package_dir(conda_recipe, py=2.7):
    cmd = ['conda', 'build', '--output', conda_recipe, '--py', str(py)]
    print("CMD", cmd)
    print('conda_recipe', conda_recipe)
    output = subprocess.check_output(cmd)
    conda_py = 'py%s' % os.getenv('CONDA_PY')
    pyver = 'py%s' % str(py).replace('.', '')
    # BUG: https://github.com/conda/conda-build/issues/3400
    return (output.decode()
            .replace('\n', '')
            .replace(conda_py, pyver))

def tar_xf(fn):
    sh('tar -xf {}'.format(fn))


def sh(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        try:
            print(e.output.decode())
        except AttributeError:
            print('e.output is ', e.output)
            pass


def update_amber():
    sh('./update_amber --show-applied-patches')
    sh('./update_amber --update')
    sh('./update_amber --show-applied-patches')


def set_compiler_env():
    if sys.platform.startswith('darwin'):
        # make sure to install gfortran
        # https://gcc.gnu.org/wiki/GFortranBinaries#MacOS
        # we do not use clang here since we still need
        # gfortran (so just use included gcc/g++)
        # os.environ['CXX'] = '/usr/local/gfortran/bin/g++'
        # os.environ['CC'] = '/usr/local/gfortran/bin/gcc'
        os.environ['FC'] = '/usr/local/gfortran/bin/gfortran'


def run_configure():
    if sys.platform.startswith('darwin'):
        sh('./configure --with-python python -macAccelerate clang')
    else:
        sh('./configure --with-python python gnu')


def make_install(ncpus=4):
    sh('make install -j%s' % str(ncpus))


def make_python_serial():
    amberhome = os.getenv('AMBERHOME') 
    os.chdir(os.path.join(amberhome, 'AmberTools/src'))
    sh('make python_serial')
    os.chdir(amberhome)


def patch(patch_fname):
    print("Patching ...")
    # We want to reuse libcpptraj from previous build.
    with open('AmberTools/src/Makefile') as fh:
        lines = [line for line in fh.readlines()
                if '$(MAKE) $(LIBCPPTRAJ)' not in line]
    with open('AmberTools/src/Makefile', 'w') as fh:
        for line in lines:
            fh.write(line)


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

    print("MINICONDA root", find_miniconda_root())
    print("ENV_PATH", env_path)
    if not os.path.exists(env_path):
        create_env(env_name, python_version)
    os.system('source activate {}'.format(env_name))

    yield

    # os.system('conda env remove -n {} -y'.format(env_name))
    os.environ['PATH'] = ORIG_PATH
