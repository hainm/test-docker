# make sure having AmberTools16.tar.bz2 file in the same folder as this Dockerfile
FROM ambermd/amber-build-box
ADD AmberTools16.tar.bz2 /usr/local/
ADD recipe/ /usr/local/amber16/

RUN     cd /usr/local/amber16 \
    &&  export AMBERHOME=$(pwd) \
    &&  ./update_amber --show-applied-patches \
    &&  ./update_amber --update \
    &&  ./update_amber --show-applied-patches \
    &&  export PATH=/opt/conda/bin:$PATH \
    &&  conda build recipe/
