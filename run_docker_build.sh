#!/usr/bin/env bash

# tar -xf A.tar.bz2
AMBER16=`pwd`/amber16
# cp -rf recipe-prebuild $AMBER16/
FEEDSTOCK_ROOT=$(cd "$(dirname "$0")/.."; pwd;)
CONDA=/root/miniconda/bin/conda
DOCKER_IMAGE=centos:6
BZ2FILE=/root/miniconda/conda-bld/linux-64/ambertools-*.tar.bz2

docker info

cat << EOF | docker run -i \
                        -v ${AMBER16}:/amber16 \
                        -v ${FEEDSTOCK_ROOT}:/feedstock_root \
                        -a stdin -a stdout -a stderr \
                        $DOCKER_IMAGE \
                        bash || exit $?

yum -y update
yum -y install gcc \
               patch \
               csh \
               flex \
               wget \
               perl \
               bzip2 \
               libgfortran44.x86_64 \
               make \
               m4 \
               which

# Embarking on 1 case(s).
    cd /amber16/
    wget http://repo.continuum.io/miniconda/Miniconda-3.7.0-Linux-x86_64.sh -O miniconda.sh;
    bash miniconda.sh -b
    export PATH=/root/miniconda/bin:\$PATH
    $CONDA update --yes --all
    $CONDA install --yes conda-build anaconda-client
    $CONDA info
    $CONDA create -n myenv python=$PYTHON_VERSION
    source activate myenv
    $CONDA build recipe-prebuild --quiet || exit 1
    echo $TRAVIS_PULL_REQUEST $TRAVIS_BRANCH
    if [[ "$TRAVIS_PULL_REQUEST" != "false" ]]; then
        echo "This is a pull request. No deployment will be done."; exit 0
    fi
    if [[ "$TRAVIS_BRANCH" != "master" ]]; then
        echo "No deployment on BRANCH='$TRAVIS_BRANCH'"; exit 0
    if
    if [[ "$TRAVIS_BRANCH" = "master" ]]; then
        anaconda upload --user hainm -t $TRAVIS_TO_ANACONDA $BZ2FILE --force || exit 0
    fi
    cp $BZ2FILE /feedstock_root/test-docker/
EOF
