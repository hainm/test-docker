#!/bin/sh

isosx=`python -c "import sys; print(sys.platform.startswith('darwin'))"`
source ${RECIPE_DIR}/../conda_tools/load_functions.sh

# copy source code
echo RECIPE_DIR $RECIPE_DIR

if [ -d ${RECIPE_DIR}/../../../AmberTools ] && [ -d ${RECIPE_DIR}/../../../test ]; then
    copy_source_code
else
    echo "This recipe must be in AmberTools/src folder"
fi

#  bugfixes
export AMBERHOME=`pwd`
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
fi

./configure --skip-python gnu

(cd AmberTools/src && make ambermini)

# from load_functions
copy_files_or_folders
