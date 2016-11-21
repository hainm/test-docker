#!/bin/sh

source scripts/download_AmberTools.sh
tar -xf AmberTools16.tar.bz2 && cp -rf recipe amber16/
sh scripts/run_docker_build.sh
