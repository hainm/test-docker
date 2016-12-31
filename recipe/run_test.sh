#!/bin/sh

amber_build_task=`$PYTHON -c "import os; print(os.getenv('AMBER_BUILD_TASK', 'ambermini').lower())"`
which python
if [ "${amber_build_task}" == "ambertools" ]; then
    python -c "import parmed; print(parmed)"
    python -c "import pytraj; pytraj.run_tests()"
    python -c "import sander; print(sander)"
    which sander
    which mdgx
    cpptraj -h
    # TODO: add more
fi

antechamber -h
tleap -h
sqm -h
acdoctor -h
am1bcc -h
atomtype -h
bondtype -h
charmmgen -h
# espgen -h
match_atomname -h
# parmcal -h # parmcal does not have -h option
parmchk -h
parmchk2 -h
prepgen -h
# reduce -Help # does reduce give exit 1 for Help?
residuegen -h
respgen -h
