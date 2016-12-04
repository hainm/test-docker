#!/bin/sh

cp ../scripts/download_AmberTools.sh .
cp -rf ../recipe .
sh download_AmberTools.sh
docker build . -t ambermd/ambertools16
rm download_AmberTools.sh
rm -rf recipe
