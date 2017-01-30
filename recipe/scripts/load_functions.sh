#!/bin/sh

function copy_source_code(){
    if [ -f ${RECIPE_DIR}/../../../mkrelease_at ]; then
        echo "build development version"
        $PYTHON ${RECIPE_DIR}/scripts/copy_ambertools.py
        release=False
    else
        echo "build release version"
        if [ -d ${RECIPE_DIR}/../../../AmberTools ]; then
            # user local AmberTools version
            cp -r ${RECIPE_DIR}/../../.. .
        fi
        # otherwise, let conda build hanlde untar AmberTools
        # in meta.yaml
        release=True
    fi
    echo "release = " $release
}

function copy_files_or_folders(){
    # info + license
    cp $AMBERHOME/README $PREFIX/README.AmberTools
    cp $AMBERHOME/AmberTools/LICENSE $PREFIX/LICENSE.AmberTools

    # store programs needed to be fixed (reduce, antechamber, ...)
    mkdir $PREFIX/bin/old
    python ${RECIPE_DIR}/scripts/patch_amberhome/copy_and_post_process_bin.py $AMBERHOME/bin $PREFIX/bin
    cp -rf $AMBERHOME/lib/* $PREFIX/lib/
    cp -rf $AMBERHOME/include/* $PREFIX/include/
    if [ ! -d $PREFIX/dat ]; then
        mkdir $PREFIX/dat
    fi
    cp -rf $AMBERHOME/dat/* $PREFIX/dat/
    
    # copy DOC
    if [ "$release" == "True" ]; then
        mkdir $PREFIX/doc/
        cp $AMBERHOME/doc/Amber*.pdf $PREFIX/doc
    fi
    
    # registration
    cp ${RECIPE_DIR}/amber_registration.py $PREFIX/bin/amber_registration
    chmod +x $PREFIX/bin/amber_registration 
}
