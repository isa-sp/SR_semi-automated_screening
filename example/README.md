# Reproducible example for the conduct of simulations on a local device

## Description
This folder contains the code to reproduce the simulations of semi-automated title-abstract screening *locally* (i.e., without High Performance Computer). 
The code can also be used to run new simulations using other datasets or using altered simulation settings.

### *code*
The following scripts are available to reproduce or run simulations:
- ```data_processing.ipynb``` to retrieve and process a set of datasets of systematic reviews
- ```simulate_datasets.py``` to simulate the semi-automated screening with the processed systematic review datasets (or any other dataset in the same format) by computing rankings
- ```process_results_example.ipynb``` to process the resulting rankings into figures and tables

### *data*
The data were derived from the publicly available data of the [CLEF eHealth Task 2019](https://github.com/CLEF-TAR/tar/tree/master/2019-TAR) (Kanoulas *et al.*, 2019).
The code in the ```data_processing.ipynb``` notebook can be used to automatically retrieve those datasets and to process those datasets into a format that can be used in the simulations by the ```simulate_datasets.py``` script.

### *envs* 
The following conda environment needs to be installed before running the codes on a local device:
- ```simulations_env.yml```
- ```simulations_env_no_builds.yml```

### *functions*
A set of functions are available that are used by the ```process_results_example.ipynb``` notebook to compute performance metrics.

### *output* 
The rankings that result from running the ```simulate_datasets.py``` script and are used by the ```data_processing.ipynb``` are stored in the output folder.

## Step-by-step instruction
### ✅ Step 1: set-up the environment
***1.1 Prerequisites***
<br> 
Make sure you have the following installed:
- Git
- Miniconda or Anaconda

***1.2 Clone the repository***

Using HTTPS:
<pre><code> git clone https://github.com/isa-sp/SR_semi-automated_screening.git </code></pre>

Or using SSH:

<pre><code> git clone git@github.com:isa-sp/SR_semi-automated_screening.git </code></pre>

Alternatively, download the ZIP archive from GitHub and extract it manually.

***1.3 Navigate to the project directory***

<pre><code> cd SR_semi-automated_screening </code></pre>

***1.4 Create and activate the conda environment***

Create the environment from the provided .yml file:

<pre><code> conda env create -f envs/simulations_env_no_builds.yml </code></pre>

Activate the environment:

<pre><code> conda activate simulations_env </code></pre>

***1.5 Verify the installation***

Make sure all dependencies are installed correctly:

<pre><code> conda list </code></pre>


### ✅ Step 2: prepare the datasets
The simulations can be conducted with any dataset. In the current reproducible example we can make use of **(a)** the pre-existing data from the [CLEF eHealth Task 2019](https://github.com/CLEF-TAR/tar/tree/master/2019-TAR) (which we also used in our own evaluation study) or **(b)** any other dataset. 
#### (a) Prepare data from the CLEF eHealth Task 2019
Open the ```data_processing.ipynb``` within the simulations_env environment. Run the notebook. The processed datasets should then be stored in the ./data/processed folder and are ready to be used in the simulations.
#### (b) Prepare other dataset(s)
In case other datasets are used, make sure they adhere to the following characteristics:
- Data structure: the data should contain at least the columns 'title' (str), 'abstract' (str), and 'label_included' (int; 1 or 0).
- Number of inclusions: the data should contain at least 10 inclusions and 10 exclusions (i.e., at least 10 1s and 10 0s in the 'label_included' column, since we use the default setting of 10 inclusions and 10 exclusions as the training data to initiate the ranking for semi-automated screening).

### ✅ Step 3: Perform simulations of semi-automated screening
Run the ```simulate_datasets.py``` script to conduct simulations of semi-automated screening using the [ASReview](https://github.com/asreview) tool (Van de Schoot *et al.*, 2021). 

<pre><code> python example/code/simulate_datasets.py </code></pre>

The script outputs the rankings based on the provided datasets in the ./data/processed folder and the settings within the script, and returns the rankings by the screening tool in the ./output/rankings folder. Currently, all settings are set to default and two modelling methods are simulated: TF-IDF with logistic regression and TF-IDF with Naive Bayes. The modeling methods and other settings that can be altered are:
- *train_model* 
- *query_model* 
- *balance_model* 
- *feature_model*
- *n_simulations*
- *n_model_update* 
- *n_prior_included*
- *n_prior_excluded*

The [documentation](https://asreview.readthedocs.io/en/stable/technical/reference/asreview.html) of the ASReview tool can be adressed for further information on these settings.

### ✅ Step 4: Process the results
Run the ```process_results_example.ipynb``` to process the resulting rankings into figures and tables to gain insight in the performance of semi-automated title-abstract screening for the simulated dataset(s) and tool settings.

  
