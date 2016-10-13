#!/bin/sh

git clone https://github.com/amber-md/pytraj
cd pytraj
git clone https://github.com/amber-md/cpptraj
cd tests
sh ../../scripts/run.sh "nosetests -vs ."
