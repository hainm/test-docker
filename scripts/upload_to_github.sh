set -e -x
git config user.name $MYUSER
git config user.email $MYEMAIL
git clone ${MYREPO_URL}
cd $MYREPO 
cp $HOME/miniconda3/conda-bld/linux-64/test*bz2 .
git add test*bz2
git commit -m 'test'
git remote add production https://${GH_TOKEN}@github.com/$MYUSER/$MYREPO
git push production master --force
