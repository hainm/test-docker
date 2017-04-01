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
    BUILD_SCRIPT=$TRAVIS_BUILD_DIR/amber$version/AmberTools/src/conda_tools/build_all.py
    mkdir $HOME/TMP
    cd $TRAVIS_BUILD_DIR/amber$version
    cp ../patch_bugfix_version.* .
    patch -p0 AmberTools/src/conda-ambermini-recipe/meta.yaml  <patch_bugfix_version.ambermini
    patch -p0 AmberTools/src/conda-ambertools-all-python/meta.yaml <patch_bugfix_version.ambertools
    cd $HOME/TMP
    python $BUILD_SCRIPT --exclude-linux -t ambermini --py 2.7
}

function build_ambertools_circleci(){
    patch_name=patch_bugfix_version.ambertools
    BUILD_SCRIPT=$HOME/ambertools-binary-build/amber$version/AmberTools/src/conda_tools/build_all.py
    mkdir $HOME/TMP
    cd $HOME/ambertools-binary-build/amber$version
    cp ../patch_bugfix_version.* .
    patch -p0 AmberTools/src/conda-ambermini-recipe/meta.yaml  <patch_bugfix_version.ambermini
    patch -p0 AmberTools/src/conda-ambertools-all-python/meta.yaml <patch_bugfix_version.ambertools
    cd $HOME/TMP
    python $BUILD_SCRIPT --exclude-osx --sudo -t ambermini --py 2.7
    python $BUILD_SCRIPT --exclude-osx --sudo
}
