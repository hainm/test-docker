#!/usr/bin/env bash

AMBER_BUILD_TASK=$1 # ambertools or ambertools_pack_all_pythons or ambermini
pyversion=$2
amberhome=$3
ambertools_binary_build_dir=$4
ambertools_version=$5
dry_run=$6 # True/False # Always the 2nd last
build_only=$7 # True/False # Always the last

DOCKER_IMAGE=ambermd/amber-build-box
BZ2FILE=/root/miniconda3/conda-bld/linux-64/amber*.tar.bz2
BUILD_ALL_SCRIPT=/ambertools-binary-build/build_all.py

echo "ambertools_binary_build_dir" $ambertools_binary_build_dir
echo "AMBER_BUILD_TASK = " $AMBER_BUILD_TASK
echo "Python version = " $pyversion
echo "amberhome" $amberhome
echo "Running docker image $DOCKER_IMAGE"
echo "Mouting $amberhome as /amberhome"
echo "Mouting $ambertools_binary_build_dir as /ambertools-binary-build"

# docker info

cat << EOF | docker run -i \
                        --rm \
                        -v ${amberhome}:/amberhome \
                        -v ${ambertools_binary_build_dir}:/ambertools-binary-build \
                        -a stdin -a stdout -a stderr \
                        $DOCKER_IMAGE \
                        bash || exit $?

    export PATH=/root/miniconda3/bin:\$PATH
    export AMBER_SRC=${amberhome}
    # conda update --all --yes
    export AMBER_BUILD_TASK=${AMBER_BUILD_TASK}
    dry_run=$dry_run
    echo "Building" \${AMBER_BUILD_TASK}

    mkdir \$HOME/TMP
    cd \$HOME/TMP

    if [ "\$dry_run" = "True" ]; then
        echo "python $BUILD_ALL_SCRIPT --exclude-osx --no-docker -t $AMBER_BUILD_TASK --exclude-non-conda-user -d \
               /amberhome -v $ambertools_version"
        python $BUILD_ALL_SCRIPT --exclude-osx --no-docker -t $AMBER_BUILD_TASK --exclude-non-conda-user -d \
               /amberhome -v $ambertools_version
    else
        python $BUILD_ALL_SCRIPT --exclude-osx --no-docker -t $AMBER_BUILD_TASK --exclude-non-conda-user \
               /amberhome -v $ambertools_version -b
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
