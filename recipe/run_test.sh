#!/bin/sh

set -e

amber_build_task=`python -c "import os; print(os.getenv('AMBER_BUILD_TASK', 'ambermini').lower())"`
echo "amber_build_task", ${amber_build_task}
which python

function test_ambermini(){
    reduce -Version
    antechamber -h
    tleap -h
    sqm -h
    acdoctor -h
    am1bcc -h
    atomtype -h
    bondtype -h
    charmmgen -h
    # espgen -h
    match_atomname -h
    # parmcal -h # parmcal does not have -h option
    parmchk -h
    parmchk2 -h
    prepgen -h
    residuegen -h
    respgen -h
}

function naive_test(){
    # those programs won't return exit 0
    which pbsa
    which rism1d
    which paramfit
    which addles
    which MMPBSA.py
}

function extra_test(){
    naive_test
    python -c "import parmed; print(parmed)"
    python -c "import pytraj; pytraj.run_tests()"
    python -c "import sander; print(sander)"
    python -c "import pdb4amber; print(pdb4amber)"
    xleap -h
    sander --version
    sander.LES --version
    mdgx --help
    cpptraj --help
    nab
    UnitCell
    resp
    parmed --help
    pdb4amber --help
}

case ${amber_build_task} in
    "ambermini")
        test_ambermini
    ;;
    "ambertools")
        test_ambermini
        extra_test
    ;;
    "pytraj"|"parmed"|"pdb4amber")
         $PYTHON -c "import ${amber_build_task}; print(${amber_build_task})"
    ;;
    "pysander")
         $PYTHON -c "import sander; print(sander)"
    ;;
    *)
        which ${amber_build_task}
    ;;
esac
