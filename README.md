- Build AmberTools conda
```
# Assume you have amber source code in $HOME/amber
# In each platform (centos-6 or macOS), perform below steps.
git clone https://github.com/Amber-MD/ambertools-binary-build/
bash ambertools-binary-build/build_all_simplified.sh $HOME/amber ambertools-binary-build
```

NOTE: If you're using gcc-4, you need to add `-norism` to configure step in https://github.com/Amber-MD/ambertools-binary-build/blob/729f4d5dffe3d3542517cb81b9cdc69b7e682c76/conda_tools/utils.py#L55
- Install AmberTools conda version
```
conda install ambertools -c ambermd
```

- Working versions
    conda-build==2.1.17
