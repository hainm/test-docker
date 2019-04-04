#!/bin/sh

# Note: Just make simple tests to ensure the programs runnable

# Comment below if you want to test this script in non-conda build
# Man, I am always confused with -z
set -ex
if [ ! -z "$CONDA_PREFIX" ]; then
    echo "Detect conda build"
    echo "unset PYTHONPATH"
    unset PYTHONPATH
else
    echo "Not conda build"
fi

function test_python(){
    return
    python -c "import parmed; print(parmed)"
    python -c "import pytraj; pytraj.run_tests()"
    python -c "import sander; print(sander)"
    python -c "import pdb4amber; print(pdb4amber)"
    parmed --help
    pdb4amber --help
}

test_python
echo "OK"
