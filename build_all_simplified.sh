#!/bin/sh

amber_src=$1
recipes_dir=$2

export AMBER_SRC=`(cd $amber_src && pwd)`
export AMBER_BUILD_TASK=ambertools
recipes_dir=`(cd $recipes_dir && pwd)`

notest='--no-test'
# notest=''

# Build full ambertools with python 2.7
conda build $recipes_dir/conda-recipe --py 2.7 $notest

# Use tarfile from above build to build python components in AmberTools
conda build $recipes_dir/conda-multi-python --py 3.5 $notest
conda build $recipes_dir/conda-multi-python --py 3.6 $notest
conda build $recipes_dir/conda-multi-python --py 3.7 $notest

# Combine all tarfiles from previous builds to create a single tarfile
# with all python versions
conda build $recipes_dir/conda-ambertools-all-python $notest # don't need to provide python version here. 
