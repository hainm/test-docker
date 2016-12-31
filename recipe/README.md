Build and install binary package locally
----------------------------------------

    cd $AMBERHOME

    # build conda package
    export AMBER_BUILD_TASK=AmberTools # if not, build ambermini.
    conda build AmberTools/src/conda-recipe --py 2.7 # or 3.4, 3.5, 3.6

    # get newly-built package dir
    tarfile=`conda build --output AmberTools/src/conda-recipe`
    echo $tarfile
    # Note: You can get $tarfile dir anytime (even before building it).

    # Install newly-built package locally
    conda install $tarfile

    # uninstall
    conda remove package_name
    e.g: conda remove ambertools


Notes
-----
- For OSX: CXX and CC are hard coded to gcc-6 for AmberTools build and 
clang is used for ambermini build. Please update it to your choice.
- Make sure to "make distclean" before building
- Make sure to install Miniconda outside $AMBERHOME to avoid circular copying.
    - Actually you can try re-use Miniconda in $AMBERHOME first since I use different script
    for copying files.
- I recommend to install Miniconda or Anaconda in $HOME
- conda-build will copy $AMBERHOME folder to its temp folder, so it will take times to
  build full package
- Development mode: we use `copy_ambertools.py` to copy its content (based on `mkrelease_at`)
  from $AMBERHOME to conda work place
- Release mode: We just simply copy whole AmberTools package
- Please try to play with ambermini first to get yourself familiar with conda-build
