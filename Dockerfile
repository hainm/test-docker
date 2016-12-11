FROM quay.io/pypa/manylinux1_x86_64
ADD scripts/install_miniconda.sh /root/
RUN yum update -y
RUN yum install -y \
            csh \
            flex \
            gcc \
            patch \
            zlib-devel \
            bzip2-devel \
            libXt-devel \
            libXext-devel \
            libXdmcp-devel
RUN cd /root/ && sh install_miniconda.sh
ENV PATH=/root/miniconda3/bin:$PATH
RUN rm /root/install_miniconda.sh
