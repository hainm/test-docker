# get directory of myself (amber.sh) and assume this dir is AMBERHOME
# Aim: We can copy amber tree to the new directory without updating amber.sh

AMBER_PREFIX="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export AMBERHOME=$AMBER_PREFIX

echo "AMBERHOME = $AMBERHOME"
export PATH="${AMBER_PREFIX}/bin:${PATH}"

python_ver=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
amber_python_path="$AMBER_PREFIX/lib/python$python_ver/site-packages/"
echo $amber_python_path
# Add location of Amber Python modules to default Python search path
#
if [ -z "$PYTHONPATH" ]; then
    export PYTHONPATH="$amber_python_path"
else
    export PYTHONPATH="$amber_python_path:${PYTHONPATH}"
fi

if [ `uname -s|awk '{print $1}'` != "Darwin" ]; then
    # Only add LD_LIBRARY_PATH for Linux
    if [ -z "${LD_LIBRARY_PATH}" ]; then
       export LD_LIBRARY_PATH="${AMBER_PREFIX}/lib"
    else
       export LD_LIBRARY_PATH="${AMBER_PREFIX}/lib:${LD_LIBRARY_PATH}"
    fi
fi
