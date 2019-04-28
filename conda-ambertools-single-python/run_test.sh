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

amber_build_task=`python -c "import os; print(os.getenv('AMBER_BUILD_TASK', 'ambertools').lower())"`
echo "amber_build_task", ${amber_build_task}
which python

function test_nab(){
    testfile="test_nab"
    nabfile="dna.nab"
    cat > $nabfile <<EOF
molecule m;
m = fd_helix( "abdna", "aaaaaaaaaa", "dna" );
putpdb( "nuc.pdb", m, "-wwpdb");
EOF
    nab $nabfile -o $testfile
    if [ ! -z "$CONDA_PREFIX" ]; then
        AMBERHOME=`python -c "import sys; print(sys.prefix)"` ./$testfile
    else
        ./$testfile
    fi
    rm $testfile $nabfile tleap.out nuc.pdb dna.c
}

function test_ambermini(){
    reduce -Version
    antechamber -h
    tleap -h
    sqm -h
    am1bcc -h
    atomtype -h
    bondtype -h
    # acdoctor -h
    # charmmgen -h
    # match_atomname -h
    espgen -h
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
    which FEW.pl
    which MCPB.py
    which xleap
}

function extra_test(){
    naive_test
    python -c "import parmed; print(parmed)"
    python -c "import pytraj; pytraj.run_tests()"
    python -c "import sander; print(sander)"
    python -c "import pdb4amber; print(pdb4amber)"
    sander --version
    sander.LES --version
    mdgx --help
    cpptraj --help
    # test_nab
    which nab
    UnitCell
    resp
    parmed --help
    pdb4amber --help
    packmol-memgen --help
}

case ${amber_build_task} in
    "ambertools")
        test_ambermini
        extra_test
        echo "OK"
    ;;
    "ambermini")
        test_ambermini
        echo "OK"
    ;;
    "nab")
        test_nab
        echo "OK"
    ;;
    "pytraj"|"parmed"|"pdb4amber")
        $PYTHON -c "import ${amber_build_task}; print(${amber_build_task})"
        echo "OK"
    ;;
    "pysander")
        $PYTHON -c "import sander; print(sander)"
        echo "OK"
    ;;
    *)
        which ${amber_build_task}
    ;;
esac
