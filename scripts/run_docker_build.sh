#!/usr/bin/env bash

FEEDSTOCK_ROOT=$(cd "$(dirname "$0")/.."; pwd;)
echo "FEEDSTOCK_ROOT" $FEEDSTOCK_ROOT
DOCKER_IMAGE=ambermd/amber-build-box
BZ2FILE=/root/miniconda3/conda-bld/linux-64/amber*.tar.bz2

docker info

cat << EOF | docker run -i \
                        --rm \
                        -v ${FEEDSTOCK_ROOT}:/feedstock_root \
                        -a stdin -a stdout -a stderr \
                        $DOCKER_IMAGE \
                        bash || exit $?

# Embarking on 1 case(s).
    export PATH=/root/miniconda3/bin:\$PATH
    conda update --all --yes
    conda build /feedstock_root/recipe --py 2.7 --quiet || exit 1
    conda build /feedstock_root/recipe --py 3.4 --quiet || exit 1
    conda build /feedstock_root/recipe --py 3.5 --quiet || exit 1
    cp $BZ2FILE /feedstock_root/
EOF
