#!/bin/bash

if [ `uname` == "Darwin" ]
then
    mkdir -p lib/amber_3rd_party # to avoid overwritten by other programs 
    $PYTHON $RECIPE_DIR/copy_and_fix_gfortran.py /usr/local/gfortran/lib lib/amber_3rd_party
    LIB=$PREFIX/lib
    mkdir -p $LIB
    cp -rf lib/amber_3rd_party $PREFIX/lib
else
    echo "Only target Darwin. Exit"
    exit 1
fi
