#!/bin/sh

echo ${AMBERHOME}
(cd ${AMBERHOME}/AmberTools/test && make test.leap)
(cd ${AMBERHOME}/AmberTools/test && make test.antechamber)
(cd ${AMBERHOME}/AmberTools/test && make test.sqm)
