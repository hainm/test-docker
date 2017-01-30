[![Build Status](https://travis-ci.org/Amber-MD/ambertools-conda-build.svg?branch=master)](https://travis-ci.org/Amber-MD/ambertools-conda-build)
[circleci](https://circleci.com/gh/Amber-MD/ambertools-conda-build)

Build AmberTools with conda and docker. This is beta version.

- Update AmberTools version

```bash
    # change v16 to v17
    python scripts/update_ambertools_version.py 16 17
```

- centos:5 derived image is used.

- Proposed usage
```bash
    conda install -c http://ambermd.org/conda/ ambertools=16

    # current working version with python=2.7 and 3.5
    conda install -c hainm ambertools=16

    # search
    anaconda search ambertools
```

- How to build

    1. Make a git commit to this repo. Circleci (and travis) will do the rest.
    Built packages can retrieved from below url:

    ```bash
        https://circleci.com/gh/Amber-MD/ambertools-conda-build/{build_number}#artifacts/containers/0
        Note: Need to replace {build_number} by the commit number
        e.g:
        https://circleci.com/gh/Amber-MD/ambertools-conda-build/153#artifacts/containers/0
    ```


    2. Or: build locally
    - by docker container
    ```bash
        # update build.sh if needed
        # build ambermini with python=2.7, 3.4, 3.5
        bash scripts/run_docker_build.sh

        # build ambertools with given python version
        bash scripts/run_docker_build.sh ambertools 2.7

        # output tar files will be in current folder
        # ls amber*tar.bz2
    ```

    - by conda
    ```bash
    # build ambermini
    conda build recipe --py 2.7

    # build full ambertools
    export AMBER_BUILD_TASK=ambertools
    conda build recipe --py 2.7

    # output tar files will be in
    # conda build --output recipe
    ```

 - How continuous integration services are being used?

     - travis : test building ambermini, full ambertools with GNU compiler, not use docker.
     - circleci: test building ambermini with our ('ambermd/amber-build-box') docker image.
     - Why? just for testing

# Minor edit conda package without rebuilding?

Since building AmberTools is time consuming, you can make minor edit by using 
```python
from scripts.edit_package import editing_conda_package

with editing_conda_package(pkg_name, output_dir='./tmp'):
    # do something here
    # e.g: add bin/new.py to package
    with open('bin/new.py', 'w') as fh:
        fh.write('print("hello there")')

# Note: not well tested
```

# Continuous integration tips

- push commit without building: 
```bash
git commit -m '[ci skip] your_message_here'
```

- use "[upload]: enter your message here" message for uploading
```bash
git commit -m 'UPLOAD: my update'
```

- circleci - LINUX build, using docker container
   - master: build ambernini and ambertools with py2.7, 3.4, 3.5
- travis - OSX build, using travis OSX image
   - master: build ambernini and ambertools with py2.7, 3.4, 3.5
