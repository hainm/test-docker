#!/bin/sh

url=$AMBERTOOLS_URL # encrypted (check circleci and travis setting)
tarfile=`python -c "url='$url'; print(url.split('/')[-1])"`
version='16'

function download_ambertools(){
    wget $url -O $tarfile
    tar -xf $tarfile
}

function build_ambertools_travis(){
    mkdir $HOME/TMP
    cd $HOME/TMP
    conda build $TRAVIS_BUILD_DIR/ambertools-binary-build/amber$version/AmberTools/src/conda-ambermini-recipe/
}

function build_ambertools_circleci(){
    mkdir $HOME/TMP
    cd $HOME/TMP
    python $HOME/ambertools-binary-build/amber$version/AmberTools/src/conda_tools/build_all.py --exclude-osx --sudo
}
