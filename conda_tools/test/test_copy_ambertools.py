import os
import sys
from mock import patch
import shutil

sys.path.insert(0, '..')
import copy_ambertools as cam


@patch('subprocess.call')
def test_copy_ambertools(mock_call):
    cwd = os.getcwd()
    tmp = 'ok_to_delete_me'
    try:
        os.mkdir(tmp)
    except OSError:
        pass
    os.chdir(tmp)

    cam.mkdir_ambertree()
    cam.copy_tree()
    os.chdir(cwd)
    assert mock_call.called
