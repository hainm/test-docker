#!/bin/sh

osname=`python -c 'import sys; print(sys.platform)'`
if [ $osname = "darwin" ]; then
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O miniconda.sh;
else
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
fi

bash miniconda.sh -b
export PATH=$HOME/miniconda3/bin:$PATH
conda install --yes conda-build jinja2 anaconda-client pip cython numpy nomkl
conda info
conda update --all --yes
