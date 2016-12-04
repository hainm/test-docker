#!/bin/sh

script=install_miniconda.sh
cp ../scripts/$script .
docker build . -t ambermd/amber-build-box
rm $script
