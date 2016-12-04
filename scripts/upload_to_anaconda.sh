# adapted slightly from ``mdtraj`` package
# coveralls

echo "pull request = " $TRAVIS_PULL_REQUEST ", branch = " $TRAVIS_BRANCH

if [[ "$TRAVIS_PULL_REQUEST" != "false" ]]; then
    echo "This is a pull request. No deployment will be done."; exit 0
fi

if [[ "$TRAVIS_BRANCH" != "master" ]]; then
    echo "No deployment on BRANCH='$TRAVIS_BRANCH'"; exit 0
fi

if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    anaconda -t $TRAVIS_TO_ANACONDA upload --force -u hainm $HOME/miniconda3/conda-bld/osx-64/amber*
fi
