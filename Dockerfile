FROM  condaforge/linux-anvil

# To get the AmberTools16.tar.bz file, fill out the form
# at the site below and click Download.
ADD A.tar.bz2 /usr/local/

RUN yum install csh -y
RUN yum install wget -y
RUN yum install gcc-gfortran -y
RUN yum install flex -y

RUN     cd /usr/local/amber16 \
    &&  export AMBERHOME=$(pwd) \
    &&  ./update_amber --show-applied-patches \
    &&  ./update_amber --update \
    &&  ./update_amber --show-applied-patches \
    &&  ./AmberTools/src/configure_python -v 3 \
    &&  export CC=/usr/bin/gcc \
    &&  ./configure -noX11 gnu \
    &&  . ${AMBERHOME}/amber.sh \
    &&  make -j4 install
