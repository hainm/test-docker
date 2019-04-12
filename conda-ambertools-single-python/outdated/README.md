Build and install binary package locally
----------------------------------------

    # NOTE: Make sure to update version number when you build the update
    # Edit meta.yaml file:
    # {% set version = "17" %}
    # {% set bugfix_version = "0" %} # update.{{bugfix_version}} # 0: None
    # {% set build_number = "0" %}
    # {% set ambertools_version = version + '.' + bugfix_version + '.' + build_number %}
    # The final version should be something like "17.1.0"

    cd $AMBERHOME
    make uninstall

    cd AmberTools/src

    # build conda package:
    export AMBER_BUILD_TASK=ambermini  # OR
    export AMBER_BUILD_TASK=ambertools # (default)
    export SKIP_REGISTRATION=1         # if desired, for testing

    conda build conda-recipe --py 2.7 # or 3.4, 3.5, 3.6
    #  (conda looks at the meta.yaml file in the above directory, and then
    #  calls build.sh.  If the build is successful, it will then call
    #  run_test.sh to run (quick) tests.)

    # get the name of the newly-built package:
    tarfile=`conda build --output $AMBERHOME/AmberTools/src/conda-recipe`
    echo $tarfile

    # Optional: primarily for local testing
    # Install newly-built package locally, i.e. into your conda
    #    sys.prefix directory, which you could get like this:
    #    export AMBERHOME=`python -c "import sys; print(sys.prefix)"`
    conda install $tarfile

    # uninstall:
    conda remove ambertools

----------------------------------------------------------------------------
# For an end-user who does not have conda installed, the following
# command will create an /opt/amber16 folder and install AmberTools16 there:

sh $AMBERHOME/AmberTools/src/conda-recipe/install_ambertools.sh --prefix /opt/
#   (what this script does:     )

----------------------------------------------------------------------------


------------------------------------------------
Build Linux and Mac versions with one single run
------------------------------------------------

Require: MacOS + docker + conda_build

What it does: uses mkrelease_at (if present) to create sources; compiles
    locally to get MacOS version; uses a local docker container to make
    the Linux versions

First, update AmberTools version, update, build numbers in 
    $AMBERHOME/AmberTools/src/conda-recipe/meta.yaml

    mkdir $HOME/TMP
    cd $HOME/TMP
    # build all python versions (2.7, 3.4, 3.5, 3.6) for both Linux and MacOS targets
    python $AMBERHOME/AmberTools/src/conda_tools/build_all.py

    # single python version
    python $AMBERHOME/AmberTools/src/conda_tools/build_all.py --py 2.7

    # dry run: trying to print the build commands without actual build
    python $AMBERHOME/AmberTools/src/conda_tools/build_all.py -d

    # print help message:
    python $AMBERHOME/AmberTools/src/conda_toolsbuild_all.py --help

    # Expected output folders in $HOME/TMP
        amber-conda-bld
             linux-64
             osx-64
             non-conda-install
    
TIPS: For small edit and testing, you can just untar the ".bz2" file,
edit its content, then tar it, zip it (.bz2) and distribute it.

Building non-conda binary packge (e.g for phenix-amber guys)
------------------------------------------------------------
- Finish the conda build step
- mkdir TMP
- cd TMP
- python conda_tools/pack_binary_without_conda_install.py /path/to/conda/AmberToolsXXX.tar.bz2

Using docker to build Linux target on MacOS host
------------------------------------------------

It's good if you want run everything in your mac and/or if you want 
     an isolated environment.

- Require: Install docker (https://docs.docker.com/docker-for-mac/)

- Build
    cd $AMBERHOME
    # login to docker container
    docker run -it --rm -v `pwd`:/work/ -w /work ambermd/amber-build-box bash
    
    # -it : interactive (so you can login to docker container terminal)
    # --rm : remove container after logging out ('cause docker will create 
    #        a separated container anytime you "run" the image
    # -v : mount folder (in this case, mounting $AMBERHOME folder as 
           /work folder in the container)
    #      You can certainly pick any folder name as you like.
    # -w : after logging, change directory to /work
    # ambermd/ambermd-build-box : docker image (based on centos 5) that Hai 
    #      built. If you don't have it, docker will pull from 
    #      dockerhub: https://hub.docker.com/r/ambermd/amber-build-box/builds/)
    # bash : enter bash terminal
    
    # then (similiar to regular build)
    cd /work/AmberTools
    export AMBER_BUILD_TASK=AmberTools
    conda build conda-recipe --py 2.7

    # You need to copy the binary to /work folder (which is your 
          $AMBERHOME directory).  For example"
    #   cp /root/miniconda3/conda-bld/linux-64/ambertools-17.0.1-py27_1.tar.bz /work
    # since you are running everything in the docker container.

    # exit docker: Ctrl-C or exit()

Upload binary packages to Anaconda
----------------------------------

If we do not set up the ambermd host yet, we can just upload to Anaconda

    ```bash
    # install anaconda-client: only do once
    conda install anaconda-client
    # upload tar files to "ambermd" channel in Anaconda
    # https://anaconda.org/ambermd
    anaconda upload /path/to/tar/file --user ambermd

    # Regular user can install ambertools via:
    conda install ambertools=17 -c ambermd

    # Ideally, we can host the tar files by ourself
    # suggested syntax
    # conda install ambertools=17 -c http://ambermd.org/conda

Run full AmberTools tests for binary distribution
-------------------------------------------------
- Require binary AmberTools tarfile + its source code (AmberTools17.tar.bz2)
- Unpack source code

- If using non-conda install:

    - Download binary tarfile, unpack it and
        source /path/to/amber17/amber.sh

- If using conda install:
    conda install /path/to/ambertools17*.tar.bz2
    export AMBERHOME=`python -c "import sys; print(sys.prefix)"`
    amber.setup_test_folders /path/to/ambertools/source/code

Example:

    source $HOME/install/amber17/amber.sh
    amber.setup_test_folders $HOME/amber_src/

- cd $AMBERHOME && make test
(Or make any test you'would like to)

amber.setup_test_folders will make some symlinks to AmberTools/test and test folder in amber source
folder.

Continous intergration
----------------------

- conda and non-conda-install packages are built on circleci (https://circleci.com/gh/Amber-MD/ambertools-test)
(nightly and commit-ly builds). There is a running script on casegroup that is checking
new amber git commit every 15 minutes. If there is a new commit, that script will make a AmberTools{version}.tar.gz
(hosted on ambermd.org), and will submit a commit to https://github.com/Amber-MD/ambertools-test, which then will
trigger build on circleci.

Collaborators and developers can download the non-conda-install (binary) package by running

    python AmberTools/src/download_circleci_AmberTools.py
    (only Linux build with python 2.7 for now)

Please check docs in AmberTools/src/download_circleci_AmberTools.py

Other conda-XXX folder in Ambertools/src
----------------------------------------

- conda-ambermini-recipe: to build ambermini that do not require specific Python verion.

- conda-ambertools-all-python, conda-multi-python: two conda-recipes that are used subsequently 
to build a binary AmberTools distribution that can be run on most of Python versions (2.7, 3.4, 3.5, 3.6).
Those two recipes are not meant to be run directly (that why I did not add "recipe" to their names).

How to build?

    python $AMBERHOME/AmberTools/src/conda_tools/build_all.py --pack-all-pythons

How to run quick test?

    python $AMBERHOME/AmberTools/src/conda_tools/test_multiple_pythons.py /path/to/AmberTols*.tar.bz2

    What does this script do? For each python version, create new conda environment, run conda-recipe/run_test.sh
    Remove that env if the test finished.

Notes
-----
- GNU compiler is used for both Linux and OSX build.

    Why not using clang on OSX (although we recommend it in website)?

    Because we still require users to install gfortran (prefer binary), so just
    use included g++/gcc to maximize compatibility. This works well so far for me.

- For OSX: CXX and CC are hard coded to gfortran dir. You can update those in ./build.sh

    export CXX=/usr/local/gfortran/bin/g++
    export CC=/usr/local/gfortran/bin/gcc
    export FC=/usr/local/gfortran/bin/gfortran

- conda-build will copy $AMBERHOME folder to its temp folder, so it will 
     take time to build full package

- Development mode: we use `copy_ambertools.py` to copy its content 
     (based on `mkrelease_at`) from $AMBERHOME to conda work place

- Release mode: We just simply copy whole AmberTools package, since
     this is presumably done using a branch like amber16-with-patches.
     Note: Should not install Miniconda in $AMBERHOME in this case to avoid circular copying
     (otherwise conda will copy miniconda to $AMBERHOME/miniconda/conda-bld/)

     TODO : update script "function copy_source_code" in "scripts/load_functions.sh" to fix.
     # Do we have a command to copy whole folder but excluding one?

     # e.g: cp -rf amber17 --exclude amber17/miniconda/?

     The main idea is
         tar xvfj AmberTools16.tar.bz2
         conda build amber17/AmberTools/src/conda-recipe
