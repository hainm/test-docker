#!/usr/bin/env bash

# PLEASE NOTE: This script was adapted from output generated by conda-smithy.

# tar -xf A.tar.bz2
AMBER16=`pwd`/amber16
# cp -rf recipe-prebuild $AMBER16/

FEEDSTOCK_ROOT=$(cd "$(dirname "$0")/.."; pwd;)

docker info

config=$(cat <<CONDARC

channels:
 - defaults # As we need conda-build

 - conda-forge

conda-build:
 root-dir: /feedstock_root/build_artefacts

show_channel_urls: true

CONDARC
)

cat << EOF | docker run -i \
                        -v ${AMBER16}:/amber16 \
                        -v ${FEEDSTOCK_ROOT}:/feedstock_root \
                        -a stdin -a stdout -a stderr \
                        condaforge/linux-anvil \
                        bash || exit $?

export PYTHONUNBUFFERED=1

echo "$config" > ~/.condarc
# A lock sometimes occurs with incomplete builds. The lock file is stored in build_artefacts.
conda clean --lock

conda update --yes --all
conda install --yes conda-build
conda info

yum -y install csh flex wget

# Embarking on 1 case(s).
    # conda build /feedstock_root/test-docker/amber16/recipe-prebuild --quiet || exit 1
    cd /amber16/
    conda build recipe-prebuild --quiet || exit 1
    cp `conda build --output recipe-prebuild` /feedstock_root/test-docker/
EOF
