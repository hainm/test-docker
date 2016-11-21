#!/usr/bin/env bash

# tar -xf A.tar.bz2
AMBER16=`pwd`/amber16
# cp -rf recipe-prebuild $AMBER16/
FEEDSTOCK_ROOT=$(cd "$(dirname "$0")/.."; pwd;)
echo "FEEDSTOCK_ROOT" $FEEDSTOCK_ROOT
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
    source /feedstock_root/scripts/install_miniconda.sh
    conda build recipe-prebuild --quiet || exit 1
    cp $BZ2FILE /feedstock_root/
EOF
