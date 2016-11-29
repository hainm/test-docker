#!/usr/bin/env bash

FEEDSTOCK_ROOT=$(cd "$(dirname "$0")/.."; pwd;)
echo "FEEDSTOCK_ROOT" $FEEDSTOCK_ROOT
DOCKER_IMAGE=ambermd/manylinux-extra
BZ2FILE=/root/miniconda3/conda-bld/linux-64/ambertools-*.tar.bz2

docker info

cat << EOF | docker run -i \
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
    source /feedstock_root/scripts/install_miniconda.sh
    conda /feedstock_root/build recipe --quiet || exit 1
    cp $BZ2FILE /feedstock_root/
EOF
