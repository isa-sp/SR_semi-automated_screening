## Reproducible example for the conduction of simulations on a local device

### Description
This folder contains the code to reproduce the simulations locally. 
The code can also be used to run new simulations using other datasets or using altered simulation settings.

### *code*
The following codes are available to reproduce/run simulations:
- ```process_datasets.ipynb``` to retrieve and process a set of datasets of systematic reviews of intervention studies
- ```simulate_datasets.py``` to simulate the semi-automated screening with the processed intervention review data (or any other dataset in the same format) by computing rankings
- ```process_example_results.ipynb``` to process the resulting rankings into figures and tables

### *data*
The data were derived from the publicly available data of the [CLEF eHealth Task 2019](https://github.com/CLEF-TAR/tar/tree/master/2019-TAR).
The code in the process_datasets.ipynb notebook can be used to automatically retrieve those datasets and processes the datasets into a format
that can be used in the simulations by the simulate_datasets.py script.

### *envs* 
The following conda environment can be used on a local device:
- ```simulations_env.yml```
- ```simulations_env_no_builds.yml```

### *functions*
A set of functions are available that are used by the process_example_results.ipynb notebook to compute performance metrics.

### *output* 
The rankings that results from running the simulate_datasets.py script and are used by the process_datasets.ipynb are stored in the output folder.
