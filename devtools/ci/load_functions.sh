#!/bin/sh

url=$AMBERTOOLS_URL # encrypted (check circleci and travis setting)
tarfile=`python -c "url='$url'; print(url.split('/')[-1])"`
version='16'

function download_ambertools(){
    wget $url -O $tarfile
    tar -xf $tarfile
}

function build_ambertools_travis(){
    # ambermini for now
    patch_name=patch_bugfix_version.ambermini
    mkdir $HOME/TMP
    cd $TRAVIS_BUILD_DIR/amber$version
    cp ../$patch_name .
    patch -p0 AmberTools/src/conda-ambermini-recipe/meta.yaml  <$patch_name
    cd $HOME/TMP
    conda build $TRAVIS_BUILD_DIR/amber$version/AmberTools/src/conda-ambermini-recipe/
}

function build_ambertools_circleci(){
    patch_name=patch_bugfix_version.ambertools
    mkdir $HOME/TMP
    cd $HOME/ambertools-binary-build/amber$version
    cp ../$patch_name .
    patch -p0 AmberTools/src/conda-recipe/meta.yaml  <$patch_name
    cd $HOME/TMP
    python $HOME/ambertools-binary-build/amber$version/AmberTools/src/conda_tools/build_all.py --exclude-osx --sudo
}
