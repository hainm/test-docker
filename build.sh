#!/bin/sh

source scripts/download_AT16.sh
tar -xf AmberTools16.tar.bz2 && cp -rf recipe-prebuild amber16/
source scripts/run_docker_build.sh