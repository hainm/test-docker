import os
import sys
from mock import patch

this_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(this_dir, '..'))

import build_ambertools

@patch('os.path.exists')
@patch('shutil.rmtree')
@patch('copy_ambertools.main')
def test_build(mock_copy_ambertools_main,
        mock_rmtree,
        mock_exists):
    prefix = os.path.abspath('./tmp')
    try:
        os.mkdir(prefix)
    except OSError:
        pass
    os.environ['RECIPE_DIR'] = os.path.join(this_dir, '..')
    os.environ['PREFIX'] = prefix
    build_ambertools.main()
