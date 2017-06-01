#!/bin/sh

isosx=`python -c "import sys; print(sys.platform.startswith('darwin'))"`
amber_build_task=`python -c "import os; print(os.getenv('AMBER_BUILD_TASK', 'ambermini').lower())"`
source ${RECIPE_DIR}/scripts/load_functions.sh
echo "amber_build_task", ${amber_build_task}

# copy source code
if [ -d ${RECIPE_DIR}/../../../AmberTools ] && [ -d ${RECIPE_DIR}/../../../test ]; then
    copy_source_code
fi

export AMBERHOME=`pwd`
#  bugfixes
./update_amber --show-applied-patches
./update_amber --update
./update_amber --show-applied-patches

# run configure
if [ "$isosx" == "True" ]; then
    # make sure to install gfortran
    # https://gcc.gnu.org/wiki/GFortranBinaries#MacOS
    # we do not use clang here since we still need
    # gfortran (so just use included gcc/g++)
    export CXX=/usr/local/gfortran/bin/g++
    export CC=/usr/local/gfortran/bin/gcc
    export FC=/usr/local/gfortran/bin/gfortran
    ./configure --with-python `which python` gnu
else
    ./configure --with-python `which python` gnu
fi

source amber.sh

# make
if [ "${amber_build_task}" == "ambertools" ]; then
    # build whole ambertools
    make install -j${CPU_COUNT}
elif [ "${amber_build_task}" == "ambermini" ]; then
    # build ambermini
    # we might adding more packages, so use build_ambermini.sh
    source ${RECIPE_DIR}/build_ambermini.sh
else
    # e.g: make sander
    case ${amber_build_task} in
        'pytraj'|'parmed'|'pymdgx'|'pysander')
            (cd AmberTools/src/ && make ${amber_build_task})
            ;;
        'pdb4amber')
            (cd AmberTools/src/ && make parmed)
            (cd AmberTools/src/ && make pdb4amber)
            ;;
        *)
            (cd AmberTools/src/${amber_build_task} && make)
            ;;
    esac
fi

if [ "$isosx" == "True" ]; then
    # fix rpath
    $PYTHON ${RECIPE_DIR}/scripts/fix_rpaths_osx.py $AMBERHOME/bin/
    $PYTHON ${RECIPE_DIR}/scripts/fix_rpaths_osx.py $AMBERHOME/lib/
fi

copy_files_or_folders
