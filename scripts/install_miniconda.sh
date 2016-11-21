#!/bin/sh

miniconda=https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
wget $miniconda -O miniconda.sh
bash miniconda.sh -b
export PATH=/root/miniconda3/bin:$PATH
conda update --yes --all
conda install --yes conda-build anaconda-client numpy matplotlib
conda info
