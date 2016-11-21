FROM  ambermd/manylinux-extra

# To get the AmberTools16.tar.bz file, fill out the form
# at the site below and click Download.
ADD AmberTools16.tar.bz2 /usr/local/
ADD recipe-prebuild/ /usr/local/amber16/

RUN yum -y update
RUN yum -y install gcc \
               patch \
               csh \
               flex \
               wget \
               perl \
               bzip2 \
               make \
               m4

RUN     cd /usr/local/amber16 \
    &&  export AMBERHOME=$(pwd) \
    &&  ./update_amber --show-applied-patches \
    &&  ./update_amber --update \
    &&  ./update_amber --show-applied-patches \
    &&  export PATH=/opt/conda/bin:$PATH \
    &&  conda build recipe-prebuild/
