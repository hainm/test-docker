#!/bin/sh

export AMBERHOME=`pwd`
yes | ./configure -noX11 gnu
source amber.sh

# build whole ambertools
# make install -j4

# build ambermini
source $RECIPE/build_ambermini.sh

# make test: add me

cp $AMBERHOME/bin/* $PREFIX/bin/
cp -rf $AMBERHOME/lib/* $PREFIX/lib/
cp -rf $AMBERHOME/include/* $PREFIX/include/
mkdir $PREFIX/dat/ && cp -rf $AMBERHOME/dat/* $PREFIX/dat/

# overwrite tleap, ...
cp $RECIPE/patch_amberhome/tleap $PREFIX/lib/
