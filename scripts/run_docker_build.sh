#!/usr/bin/env bash

echo "CIRCLE_BRANCH", $CIRCLE_BRANCH

buildfull=`python -c "import os;  print(os.getenv('CIRCLE_BRANCH').startswith('circleci_'))"`
echo 'buildfull = ' $buildfull

if [ "$buildfull" == "True" ]; then
    AMBER_BUILD_TASK='ambertools'
    pyversion=`python -c "import os; env=os.getenv('CIRCLE_BRANCH'); print(env.strip('circleci_'))"`
    echo "pyversion = " $pyversion
else
    AMBER_BUILD_TASK='ambermini'
fi

echo "AMBER_BUILD_TASK = " $AMBER_BUILD_TASK

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

    export PATH=/root/miniconda3/bin:\$PATH
    conda update --all --yes
    export AMBER_BUILD_TASK=${AMBER_BUILD_TASK}
    if [ "\${AMBER_BUILD_TASK}" == 'ambermini' ]; then
        # build in a single containter
        conda build /feedstock_root/recipe --py 2.7 --quiet || exit 1
        conda build /feedstock_root/recipe --py 3.4 --quiet || exit 1
        conda build /feedstock_root/recipe --py 3.5 --quiet || exit 1
    else
        # build whole ambertools, for a single python version
        # should build each ambertools python version on each branch
        conda build /feedstock_root/recipe --py $pyversion --quiet || exit 1
    cp $BZ2FILE /feedstock_root/
EOF
