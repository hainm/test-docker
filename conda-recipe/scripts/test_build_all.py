# run with
#    all tests: pytest test_build_all.py 
#    function test: pytest test_build_all.py::test_editing_package
#    (and so on)
# Run this test avoid running the real lengthy build
import os
from contextlib import contextmanager
import tempfile
from shutil import rmtree
import subprocess

from edit_package import editing_conda_package

@contextmanager
def tempfolder():
  """run everything in temp folder
  """
  my_temp = tempfile.mkdtemp()
  cwd = os.getcwd()
  os.chdir(my_temp)
  yield
  os.chdir(cwd)
  rmtree(my_temp)

def sh(command):
    subprocess.call(command, shell=True)

info_example = """
{
  "arch": "x86_64",
  "build": "py27_1",
  "build_number": 1,
  "depends": [
    "bzip2",
    "numpy",
    "python 2.7*",
    "requests",
    "zlib"
  ],
  "license": "GNU General Public License (GPL)",
  "name": "ambertools",
  "platform": "osx",
  "subdir": "osx-64",
  "version": "17.0.1"
}
""".strip()

def test_editing_package():
    # editing_conda_package(pkg_name, output_dir='./tmp', prefix=None)

    with tempfolder():
        sh("mkdir bin lib dat info include")
        with open('info/index.json', 'w') as fh:
            fh.write(info_example)
        sh("cat info/index.json")
        sh("tar cf test.tar bin lib dat info include")
        pkg_name = os.path.abspath('test.tar')
        output_dir = 'non-conda-install'
        with editing_conda_package(pkg_name, output_dir=output_dir):
            pass
        os.path.exists(output_dir)

def test_packing_package_for_non_conda_user():
    # If you move this file from conda-recipe folder, make sure
    # to update recipe_dir below
    recipe_dir = os.path.abspath(os.path.dirname(__file__))

    py_versions = ['27', '34', '35', '36']
    ambertools_template = 'ambertools-17.0.1-py{}_1.tar.bz2'

    with tempfolder():
        sh("mkdir linux-64")
        sh("mkdir osx-64")

        for py in py_versions:
            at = ambertools_template.format(py)
            sh("touch linux-64/{}".format(at))
            sh("touch osx-64/{}".format(at))
            sh("ls */*")
