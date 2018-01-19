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
    # acdoctor -h # turn off
    # charmmgen -h # turn off
    # match_atomname -h
    am1bcc -h
    atomtype -h
    bondtype -h
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

function test_python(){
    python -c "import parmed; print(parmed)"
    python -c "import pytraj; pytraj.run_tests()"
    python -c "import sander; print(sander)"
    python -c "import pdb4amber; print(pdb4amber)"
    parmed -h
    pdb4amber -h
}

function extra_test(){
    naive_test
    sander --version
    sander.LES --version
    mdgx --help
    cpptraj --help
    # test_nab
    which nab
    UnitCell
    resp
    which parmed
    which pdb4amber
}

test_ambermini
extra_test
echo "OK"
