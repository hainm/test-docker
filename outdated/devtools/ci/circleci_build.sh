#!/bin/sh

source devtools/ci/load_functions.sh
download_ambertools
build_ambertools_circleci


ls $HOME/TMP/amber-conda-bld/non-conda-install
files=`ls $HOME/TMP/amber-conda-bld/non-conda-install/linux-64.ambertools-*.tar.bz2`

if [ "$files" = "" ]; then
    echo "No linux-64.ambertools-*.tar.bz2. Build failed"
    exit 1
fi
