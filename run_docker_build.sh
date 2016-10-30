#!/usr/bin/env bash

# tar -xf A.tar.bz2
AMBER16=`pwd`/amber16
# cp -rf recipe-prebuild $AMBER16/
FEEDSTOCK_ROOT=$(cd "$(dirname "$0")/.."; pwd;)
CONDA=/root/miniconda/bin/conda
DOCKER_IMAGE=centos:5

docker info

cat << EOF | docker run -i \
                        -v ${AMBER16}:/amber16 \
                        -v ${FEEDSTOCK_ROOT}:/feedstock_root \
                        -a stdin -a stdout -a stderr \
                        $DOCKER_IMAGE \
                        bash || exit $?

yum -y update
yum -y install gcc patch csh flex wget perl \
               bzip2 libgfortran44.x86_64 \
               make \
               which

# Embarking on 1 case(s).
    cd /amber16/
    wget http://repo.continuum.io/miniconda/Miniconda-3.7.0-Linux-x86_64.sh -O miniconda.sh;
    bash miniconda.sh -b
    export PATH=/root/miniconda/bin:\$PATH
    $CONDA update --yes --all
    $CONDA install --yes conda-build
    $CONDA info
    $CONDA build recipe-prebuild --quiet || exit 1
    cp `$CONDA build --output recipe-prebuild` /feedstock_root/test-docker/
EOF
