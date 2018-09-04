## Running the data analysis workflow

The data analysis is described as a [snakemake](https://snakemake.readthedocs.io/en/stable/) workflow. To run the full data analysis from scratch run:
```
snakemake clean
snakemake
```
The analysis can be run using multiple cores with `--cores=n` or `-j`. e.g. to run on all available cores:
```
snakemake -j
```
Workflows for particular sets of analysis are desribed in `*.smk` files:
- `rdfs.smk`
- `sites.smk`
- `diffusion.smk`
A particular sub-analysis can be run using `--snakefile`, e.g. to run only the rdf analysis:
```
snakemake --snakefile rdfs.smk rdfs_clean
snakemake --snakefile rdfs.smk
```

## Dependencies
The analysis workflow has the following Python module dependencies:
```
TODO
```
These can be installed using `pip` via
```
pip install -r requirements.txt
```

## Runtime environment and frozen dependencies
Details about the runtime environement and the versions of installed python modules are saved to `system_info.txt`

