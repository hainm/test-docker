FROM  python:3.5.2

# To get the AmberTools16.tar.bz file, fill out the form
# at the site below and click Download.
ADD A.tar.gz /usr/local/

RUN     apt-get update \
    &&  apt-get install -y \
        csh \
        flex \
        gfortran \
        g++ \
        zlib1g-dev \
        libbz2-dev \
        patch \
        openmpi-bin \
        libopenmpi-dev
   
RUN     cd /usr/local/amber16 \
    &&  export AMBERHOME=$(pwd) \
    &&  ./update_amber --show-applied-patches \
    &&  ./update_amber --update \
    &&  ./update_amber --show-applied-patches \
    &&  ./AmberTools/src/configure_python \
    &&  ./configure -noX11 gnu \
    &&  . ${AMBERHOME}/amber.sh \
    &&  make -j4 install \
    &&  ./configure -noX11 -mpi gnu \
    &&  make -j4 install 
