#!/bin/sh

export AMBERHOME=`pwd`
yes | ./configure -noX11 gnu
# debug
cat AmberTools/src/netcdf-4.3.0/netcdf.c.compile.log
# 
source amber.sh
make install -j4
cp $AMBERHOME/bin/* $PREFIX/bin/
cp -rf $AMBERHOME/lib/* $PREFIX/lib/
mkdir $PREFIX/dat/ && cp -rf $AMBERHOME/dat/* $PREFIX/dat/
