#!/bin/sh

export AMBERHOME=`pwd`
yes | ./configure -noX11 gnu
source amber.sh
make install -j4
cp $AMBERHOME/bin/* $PREFIX/bin/
cp -rf $AMBERHOME/lib/* $PREFIX/lib/
mkdir $PREFIX/dat/ && cp -rf $AMBERHOME/dat/* $PREFIX/dat/
