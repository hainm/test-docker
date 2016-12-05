git config user.name "Travis CI"
git config user.email "travis@domain.com"
git commit -m "built with love by travis <3"
git clone ${MYREPO_URL}
cd $MYREPO 
cp $HOME/miniconda3/conda-bld/linux-64/test*bz2 .
git add test*bz2
git commit -m 'test'
git remote add production https://${GH_TOKEN}@github.com/$MYUSER/$MYREPO
git push production master --force
