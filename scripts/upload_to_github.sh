git clone ${MYREPO_URL}
cd $MYREPO 
git config user.name $MYUSER
git config user.email $MYEMAIL
cp $HOME/miniconda*/conda-bld/*/amber*bz2 .
git add amber*bz2
# cp $HOME/miniconda*/conda-bld/*/test*bz2 .
# git add test*bz2
git commit -m 'from travis build number: ${TRAVIS_BUILD_NUMBER}'
git remote add production https://${GITHUB_TOKEN}@github.com/$MYUSER/$MYREPO >& log
git push production master --force >& log
