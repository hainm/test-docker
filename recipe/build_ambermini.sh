#!/bin/sh

(cd ${AMBERHOME}/AmberTools/src/leap && make install)
(cd ${AMBERHOME}/AmberTools/src/sqm && make install)
(cd ${AMBERHOME}/AmberTools/src/antechamber && make install)
(cd ${AMBERHOME}/AmberTools/src/reduce && make install)
(cd ${AMBERHOME}/AmberTools/src/paramfit && make install)
