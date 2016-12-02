FROM  ambermd/manylinux-build-box

# To get the AmberTools16.tar.bz file, fill out the form
# at the site below and click Download.
ADD AmberTools16.tar.bz2 /usr/local/
ADD recipe/ /usr/local/amber16/

RUN     cd /usr/local/amber16 \
    &&  export AMBERHOME=$(pwd) \
    &&  ./update_amber --show-applied-patches \
    &&  ./update_amber --update \
    &&  ./update_amber --show-applied-patches \
    &&  export PATH=/opt/conda/bin:$PATH \
    &&  conda build recipe/
