#!/usr/bin/env bash

# tar -xf A.tar.bz2
AMBER16=`pwd`/amber16
# cp -rf recipe-prebuild $AMBER16/
FEEDSTOCK_ROOT=$(cd "$(dirname "$0")/.."; pwd;)
CONDA=/root/miniconda3/bin/conda
DOCKER_IMAGE=ambermd/manylinux-extra
BZ2FILE=/root/miniconda3/conda-bld/linux-64/ambertools-*.tar.bz2

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
               make \
               m4

# Embarking on 1 case(s).
    cd /amber16/
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b
    export PATH=/root/miniconda3/bin:\$PATH
    $CONDA update --yes --all
    $CONDA install --yes conda-build anaconda-client
    $CONDA info
    $CONDA build recipe-prebuild --quiet || exit 1
    cp $BZ2FILE /feedstock_root/test-docker/
EOF
