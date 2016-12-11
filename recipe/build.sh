#!/bin/sh

isosx=`python -c "import sys; print(sys.platform.startswith('darwin'))"`
build_task=`python -c "import os; print(os.getenv('AMBER_BUILD_TASK'))"`
echo "amber_build_task", ${build_task}

export AMBERHOME=`pwd`
./update_amber --show-applied-patches
./update_amber --update
./update_amber --show-applied-patches
if [ "$isosx" == "True" ]; then
    # ./configure -noX11 --with-python `which python` -macAccelerate clang

    # TODO: clang? (got EMIL error)
    export CXX=/usr/local/Cellar/gcc/6.2.0/bin/g++-6
    export CC=/usr/local/Cellar/gcc/6.2.0/bin/gcc-6
    ./configure -noX11 --with-python `which python` gnu
else
    ./configure --with-python `which python` gnu
fi
source amber.sh

if [ ${build_task} == 'ambertools' ]; then
    # build whole ambertools
    make install -j4
else
    # build ambermini
    source $RECIPE_DIR/build_ambermini.sh
fi

cp $AMBERHOME/bin/* $PREFIX/bin/
python $RECIPE_DIR/patch_amberhome/copy_and_post_process_bin.py
cp -rf $AMBERHOME/lib/* $PREFIX/lib/
cp -rf $AMBERHOME/include/* $PREFIX/include/
mkdir $PREFIX/dat/ && cp -rf $AMBERHOME/dat/* $PREFIX/dat/

# overwrite tleap, ...
# handle tleap a bit differently since it requires -I flag
# TODO: move to copy_and_post_process_bin.py?
cp $RECIPE_DIR/patch_amberhome/tleap $PREFIX/bin/

# DOC
mkidr $PREFIX/doc/
cp $AMBERHOME/doc/Amber*.pdf $PREFIX/doc

# make test: add me
if [ ${build_task} == 'ambermini' ]; then
    sh $RECIPE_DIR/run_test_inside_amberhome.sh
fi

# registration
cp $RECIPE_DIR/amber_registration.py $PREFIX/bin/amber_registration
chmod +x $PREFIX/bin/amber_registration 
