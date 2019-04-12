import os
import sys
from mock import patch
import shutil

sys.path.insert(0, '..')
import copy_ambertools as cam

this_path = os.path.join(os.path.dirname(__file__))

@patch('copy_ambertools._copy_folder')
@patch('os.getenv')
def test_copy_ambertools(mock_getenv, mock_copy):
    fake_amberhome = os.path.join(this_path, 'fake_data', 'fake_amber')
    ambertools_src = os.path.join(fake_amberhome, 'AmberTools')
    def side_effect(name, *args, **kwargs):
        if name == 'AMBER_SRC':
            return fake_amberhome
        elif name == 'RECIPE_DIR':
            return os.path.join(this_path, '..', '..', 'conda-ambertools-single-python')
    mock_getenv.side_effect = side_effect
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
    mock_copy.assert_called_with(os.path.join(fake_amberhome, 'linux-64'), '.')
