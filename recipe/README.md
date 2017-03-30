NOTE: Outdated recipe

Build and install binary package locally
----------------------------------------

    cd $AMBERHOME

    # build conda package:
    export AMBER_BUILD_TASK=AmberTools # OR
    export AMBER_BUILD_TASK=ambermini  # (default)
    export SKIP_REGISTRATION=1         # if desired, for testing
    conda build AmberTools/src/conda-recipe --py 2.7 # or 3.4, 3.5, 3.6

    # get the name of the newly-built package:
    tarfile=`conda build --output AmberTools/src/conda-recipe`
    echo $tarfile
    # Note: You can get $tarfile anytime (even before building it).

    # Install newly-built package locally (i.e. into your conda
    #    sys.prefix directory:
    prefix=`python -c "import sys; print(sys.prefix)"`
    conda install $tarfile

    # uninstall:
    conda remove package_name
    e.g: conda remove ambertools

    # You can also create a new conda env to test to avoid overwrite your main env
    conda create -n test_amber python=2.7 numpy nomkl
    source activate test_amber
    conda install $tarfile
    prefix=`python -c "import sys; print(sys.prefix)"`
    echo $prefix

    # exit `test_amber` env
    source deactivate

    # remove `test_amber` env if you do not need it
    conda env remove -n test_amber

    # For an end-user who does not  have conda installed:
    # Check ./setup-scripts/README.md
    #  Hai: can you copy the appropriate scripts here and add instructions?

Notes
-----
- BUG: If you run conda build in $AMBERHOME root folder
conda-build will delete files/folders in $AMBERHOME/dat (I am not sure why).

To avoid this, just:

    ```bash
    cd $AMBERHOME/AmberTools/src
    conda build conda-recipe
    ```

- For OSX: CXX and CC are hard coded to gcc-6 for AmberTools build and 
     clang is used for ambermini build. Please update it to your choice.
- Make sure to "make uninstall" before building
- I recommend to install Miniconda or Anaconda in $HOME
- conda-build will copy $AMBERHOME folder to its temp folder, so it will 
     take time to build full package
- Development mode: we use `copy_ambertools.py` to copy its content 
     (based on `mkrelease_at`) from $AMBERHOME to conda work place
- Release mode: We just simply copy whole AmberTools package
- Please play with ambermini first to get yourself familiar with conda-build
