#!/usr/bin/env bash

AMBER_BUILD_TASK=$1 # ambertools or ambertools_pack_all_pythons or ambermini
pyversion=$2
dry_run=$3 # True/False
    
echo "AMBER_BUILD_TASK = " $AMBER_BUILD_TASK
echo "Python version = " $pyversion

amberhome=$(cd "$(dirname "$0")/../../../../../"; pwd;)
echo "amberhome" $amberhome
DOCKER_IMAGE=ambermd/amber-build-box
BZ2FILE=/root/miniconda3/conda-bld/linux-64/amber*.tar.bz2
BUILD_ALL_SCRIPT=/amberhome/AmberTools/src/ambertools-binary-build/conda_tools/build_all.py

echo "Running docker image $DOCKER_IMAGE"
echo "Mouting $amberhome as /amberhome"

# docker info

cat << EOF | docker run -i \
                        --rm \
                        -v ${amberhome}:/amberhome \
                        -a stdin -a stdout -a stderr \
                        $DOCKER_IMAGE \
                        bash || exit $?

    export PATH=/root/miniconda3/bin:\$PATH
    # conda update --all --yes
    export AMBER_BUILD_TASK=${AMBER_BUILD_TASK}
    dry_run=$dry_run
    echo "Building" \${AMBER_BUILD_TASK}

    mkdir \$HOME/TMP
    cd \$HOME/TMP

    if [ "\$dry_run" = "True" ]; then
        python $BUILD_ALL_SCRIPT --py $pyversion --exclude-osx --no-docker -t $AMBER_BUILD_TASK --exclude-non-conda-user -d
    else
        python $BUILD_ALL_SCRIPT --py $pyversion --exclude-osx --no-docker -t $AMBER_BUILD_TASK --exclude-non-conda-user
    fi

    if [ ! -d /amberhome/linux-64/ ]; then
        mkdir /amberhome/linux-64
    fi
    # to avoid ovewriting MacOS build (we run a bunch of builds)
    if [ "\$dry_run" = "True" ]; then
        echo "cp $BZ2FILE /amberhome/linux-64/"
    else
        cp $BZ2FILE /amberhome/linux-64/
    fi
EOF
