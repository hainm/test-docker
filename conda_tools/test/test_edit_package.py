# pytest -vs .

import os
import sys
from mock import patch

sys.path.insert(0, '..')
from edit_package import editing_conda_package

this_dir = os.path.dirname(__file__)
FAKE_TAR = os.path.join(this_dir, 'fake_data', 'fake_osx.tar.bz2')


def test_output_as_conda_package():
    pkg_name = FAKE_TAR
    output_dir = 'tmp/conda/osx-64'
    with editing_conda_package(pkg_name,
                          output_dir=output_dir,
                          prefix=None,
                          add_date=False,
                          dry_run=False,
                          conda=True):
        pass
    expected_fn = os.path.join(output_dir, os.path.basename(pkg_name))
    assert os.path.exists(expected_fn)


def test_output_as_non_conda_package():
    pkg_name = FAKE_TAR
    output_dir = 'tmp/non-conda/'
    with editing_conda_package(pkg_name,
                          output_dir=output_dir,
                          prefix=None,
                          add_date=False,
                          dry_run=False,
                          conda=False):
        pass
    expected_fn = os.path.join(output_dir, 'osx-64.' + os.path.basename(pkg_name))
    assert os.path.exists(expected_fn)
