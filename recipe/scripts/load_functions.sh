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
    cp $AMBERHOME/bin/* $PREFIX/bin/
    python ${RECIPE_DIR}/scripts/patch_amberhome/copy_and_post_process_bin.py
    cp -rf $AMBERHOME/lib/* $PREFIX/lib/
    cp -rf $AMBERHOME/include/* $PREFIX/include/
    mkdir $PREFIX/dat/ && cp -rf $AMBERHOME/dat/* $PREFIX/dat/
    
    # overwrite tleap, ...
    # handle tleap a bit differently since it requires -I flag
    # TODO: move to copy_and_post_process_bin.py?
    cp ${RECIPE_DIR}/scripts/patch_amberhome/tleap $PREFIX/bin/
    
    if [ "${amber_build_task}" == "ambertools" ]; then
        cp ${RECIPE_DIR}/scripts/patch_amberhome/xleap $PREFIX/bin/
        cp $AMBERHOME/bin/nab $PREFIX/bin/_nab
        cp ${RECIPE_DIR}/scripts/patch_amberhome/nab $PREFIX/bin/
    fi
    
    # copy DOC
    if [ "$release" == "True" ]; then
        mkdir $PREFIX/doc/
        cp $AMBERHOME/doc/Amber*.pdf $PREFIX/doc
    fi
    
    # registration
    cp ${RECIPE_DIR}/amber_registration.py $PREFIX/bin/amber_registration
    chmod +x $PREFIX/bin/amber_registration 
}
