#!/bin/sh

# Example:
# bash build_all_simplified.sh $HOME/amber_git/amber $HOME/ambertools-binary-build

# Tested with
# conda 4.6.7
# conda-build 3.17.8

# NOTE: Make sure to update ambertools version in conda-ambertools-all-python/meta.yaml
# You don't need to udpate other recipes.

amber_src=$1
recipes_dir=$2 # root folder having multile recipes (below)

export AMBER_SRC=`(cd $amber_src && pwd)`
export AMBER_BUILD_TASK=ambertools
recipes_dir=`(cd $recipes_dir && pwd)`

notest='--no-test'

# Build full ambertools with python 2.7
# Do not change python version here since the subsequent steps will use
# the tarfile from python 2.
conda build $recipes_dir/conda-recipe --py 2.7 $notest || exit 1

# Use tarfile from above build to build only python components in AmberTools
# with multiple python versions
for pyver in 3.4 3.5 3.6 3.7; do
    conda build $recipes_dir/conda-multi-python --py $pyver $notest || exit 1
done

# Combine all tarfiles from previous builds to create a single tarfile
# with all python versions + non-python components
conda build $recipes_dir/conda-ambertools-all-python $notest # don't need to provide python version here. 
