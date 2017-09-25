set -ex
version=16
tarfile=amber$version.tar
platform=`python -c '
import sys
if sys.platform.startswith("darwin"):
    print("osx-64")
else: print("linux-64")
'`
prefix=tmp_${platform}_AT

cd $HOME
git clone https://github.com/$AT_GH_USER/$AT_GH_REPO_BINARY_DEV
git config --global user.email "$AT_GH_EMAIL" > /dev/null 2>&1
git config --global user.name "$AT_GH_USER" > /dev/null 2>&1
cp $HOME/ambertools-binary-build/conda_tools/amber.py27.sh $HOME/amber${version}/amber.sh

if [ "$TRAVIS" = "true" ]; then
    msg="travis build $TRAVIS_BUILD_NUMBER"
    tar -cf $tarfile amber$version/{amber.sh,bin,lib,include,dat}
    gzip $tarfile
fi

if [ "$CIRCLECI" = "true" ]; then
    msg="circle build $CIRCLE_BUILD_NUM, from $CIRCLE_BUILD_URL"
    cp $CIRCLE_ARTIFACTS/ambertools-build/non-conda-install/linux-64.*.tar.bz2 \
        $HOME/$tarfile.gz
fi

cd $AT_GH_REPO_BINARY_DEV
split -b 40000000 $HOME/$tarfile.gz $prefix
git add ${prefix}*
ls ${prefix}*

git commit -m "$msg"
git remote add production https://${AT_GH_TOKEN}@github.com/$AT_GH_USER/$AT_GH_REPO_BINARY_DEV
git push production master
