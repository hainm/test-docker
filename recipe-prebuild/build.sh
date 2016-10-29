#!/bin/sh

cp $AMBERHOME/bin/* $PREFIX/bin/
cp -rf $AMBERHOME/lib/ $PREFIX/lib/
mkdir $PREFIX/dat/ && cp -rf $AMBERHOME/dat/* $PREFIX/dat/
