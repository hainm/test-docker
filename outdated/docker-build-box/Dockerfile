FROM quay.io/pypa/manylinux1_x86_64
ADD scripts/install_miniconda.sh /root/
RUN yum update -y
RUN yum install -y \
            csh \
            flex \
            gcc \
            patch \
            zlib-devel \
            bzip2-devel
RUN cd /root/ && sh install_miniconda.sh
RUN rm /root/install_miniconda.sh
