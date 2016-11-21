Build AmberTools with conda and docker. This is beta version.

- Update AmberTools version

```bash
    # change v16 to v17
    python scripts/update_ambertools_version.py 16 17
```

- centos:5 derived image is used.

- Proposed usage
```bash
    conda install -c ambermd ambertools=16

    # current working version with python=3.5
    conda install -c hainm ambertools=16

    # search
    anaconda search ambertools
```
