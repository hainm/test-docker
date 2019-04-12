source ./scripts/check_deployment.sh
if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    echo "uploading to anaconda channel"
    anaconda -t $TRAVIS_TO_ANACONDA upload --force -u hainm $HOME/miniconda3/conda-bld/osx-64/amber*bz2 -l rc
fi
