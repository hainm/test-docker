#!/bin/sh

function copy_source_code(){
    if [ -f ${RECIPE_DIR}/../../../../mkrelease_at ]; then
        echo "build development version"
        $PYTHON ${RECIPE_DIR}/../conda_tools/copy_ambertools.py
        release=False
    else
        echo "build release version"
        if [ -d ${RECIPE_DIR}/../../../../AmberTools ]; then
            # user local AmberTools version
            cp -r ${RECIPE_DIR}/../../../.. .
        fi
        # otherwise, let conda build hanlde untar AmberTools
        # in meta.yaml
        release=True
    fi
    echo "release = " $release
}

function write_amber_sh() {
    pyver=`python -c "import sys; print('.'.join(str(x) for x in sys.version_info[:2]))"`
    cat ${RECIPE_DIR}/../conda_tools/amber.sh | sed "s/pythonX.Y/python$pyver/" > $PREFIX/amber.sh
    chmod +x $PREFIX/amber.sh
}

function copy_files_or_folders(){
    # info + license
    if [ -f $AMBERHOME/README ]; then
        cp $AMBERHOME/README $PREFIX/README.AmberTools
    elif [ -f README.AmberTools ]; then
        cp README.AmberTools $PREFIX/
    fi

    if [ -f $AMBERHOME/AmberTools/LICENSE ]; then
        cp $AMBERHOME/AmberTools/LICENSE $PREFIX/LICENSE.AmberTools
    elif [ -f LICENSE.AmberTools ]; then
        cp LICENSE.AmberTools $PREFIX/
    fi

    # store programs needed to be fixed (reduce, antechamber, ...)
    if [ -f $AMBERHOME/bin/amber.python ]; then
        rm $AMBERHOME/bin/amber.python
    fi

    # bin
    cp -rf $AMBERHOME/bin/* $PREFIX/bin/
    if [ -f $AMBERHOME/AmberTools/src/configure_python ]; then
        cp -rf $AMBERHOME/AmberTools/src/configure_python $PREFIX/bin/
    fi
    cp $RECIPE_DIR/../conda_tools/amber.setup_test_folders $PREFIX/bin/
    cp $RECIPE_DIR/../conda_tools/amber.run_tests $PREFIX/bin/

    # Lib
    cp -rf $AMBERHOME/lib/* $PREFIX/lib/

    # include
    cp -rf $AMBERHOME/include/* $PREFIX/include/

    # dat
    if [ ! -d $PREFIX/dat ]; then
        mkdir $PREFIX/dat
    fi
    cp -rf $AMBERHOME/dat/* $PREFIX/dat/
    
    # doc TODO: uncomment
    if [ "$release" == "True" ]; then
        mkdir $PREFIX/doc/
        # turn off for now
        # cp $AMBERHOME/doc/Amber*.pdf $PREFIX/doc
    fi

    # registration
    # cp ${RECIPE_DIR}/amber_registration.py $PREFIX/bin/amber_registration
    # chmod +x $PREFIX/bin/amber_registration 

    write_amber_sh
}
