pytest -vs . --cov-report=html --cov=copy_ambertools --cov=edit_package \
    --cov=fix_conda_gfortran_linking_osx --cov=pack_binary_without_conda_install \
    --cov=update_gfortran_libs_osx -n 4
