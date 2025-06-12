## Reproducible example for the conduction of simulations on a local device

### Description
This folder contains the code to reproduce the simulations of semi-automated title-abstract screening locally. 
The code can also be used to run new simulations using other datasets or using altered simulation settings.

### Folder structure
#### *code*
The following codes are available to reproduce/run simulations:
- ```process_datasets.ipynb``` to retrieve and process a set of datasets of systematic reviews of intervention studies
- ```simulate_datasets.py``` to simulate the semi-automated screening with the processed intervention review data (or any other dataset in the same format) by computing rankings
- ```process_example_results.ipynb``` to process the resulting rankings into figures and tables

#### *data*
The data were derived from the publicly available data of the [CLEF eHealth Task 2019](https://github.com/CLEF-TAR/tar/tree/master/2019-TAR).
The code in the ```process_datasets.ipynb``` notebook can be used to automatically retrieve those datasets and to process those datasets into a format that can be used in the simulations by the ```simulate_datasets.py``` script.

#### *envs* 
The following conda environment can be used on a local device:
- ```simulations_env.yml```
- ```simulations_env_no_builds.yml```

#### *functions*
A set of functions are available that are used by the ```process_example_results.ipynb``` notebook to compute performance metrics.

#### *output* 
The rankings that results from running the ```simulate_datasets.py``` script and are used by the ```process_datasets.ipynb``` are stored in the output folder.

### Step-by-step 
#### Step 1: set-up the environment


#### Step 2: prepare the datasets
The simulations can be conducted with any dataset. In this example we can make use of **(a)** the pre-existing data from the [CLEF eHealth Task 2019](https://github.com/CLEF-TAR/tar/tree/master/2019-TAR) or **(b)** any other dataset. 
##### (a) Prepare data from the CLEF eHealth Task 2019
Open the ```process_datasets.ipynb``` within the simulations_env environment. Run the notebook. The processed datasets should then be stored in the ./data/processed folder and are ready to be used in the simulations.
##### (b) Prepare other dataset(s)
In case other datasets are used, make sure they adhere to the following characteristics:
- Data structure: the data should contain at least the columns 'title' (str), 'abstract' (str), and 'label_included' (int; 1 or 0).
- Number of inclusions: the data should contain at least 10 inclusions and 10 exclusions (i.e., at least 10 1s and 10 0s in the 'label_included' column, since we use the default setting of 10 inclusions and 10 exclusions as the training data to initiate the ranking for semi-autoamted screening.

#### Step 3: perform simulations of semi-automated screening
Run the ```simulate_datasets.py``` script to conduct simulations of semi-automated screening using the [ASReview](https://github.com/asreview) tool. The script outputs the rankings based on the provided datasets in the data/processed folder and the settings within the script. Currently, all settings are set to default and two modelling methods are simulated: tf-idf with logistic regression and tf-idf with naive bayes. The modeling methods and other settings that can be altered are:
- train_model 
- query_model 
- balance_model 
- feature_model
- n_simulations 
- n_model_update 
- n_prior_included
- n_prior_excluded

The [documentation](https://asreview.readthedocs.io/en/stable/technical/reference/asreview.html) of the ASReview tool can be adressed for further documentation of these settings.

  
