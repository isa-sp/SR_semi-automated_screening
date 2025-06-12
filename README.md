# Evaluation of semi-automated record screening methods for systematic reviews of prognosis studies and intervention studies

### Description
This repository contains the code of a simulation study on semi-automated title-abstract screening for systematic reviews of prognosis and intervention studies using the [ASReview](https://github.com/asreview) tool. The repository will be further updated upon publication of the corresponding manuscript:  

**I. Spiero, A.M. Leeuwenberg, K.G.M. Moons, L. Hooft, J.A.A. Damen (2025). Evaluation of semi-automated record screening methods for systematic reviews of prognosis studies and intervention studies.** ___Accepted___


### Code (original scripts)
The simulations were run in parallel on a High Performance Computer (HPC) using the codes in the ./code folder:
- ```simulate_original_datasets.py```
- ```simulate_adapted_datasets.py```
  
The derived output was processed locally:
- ```process_results.ipynb```


### Example (reproducible scripts)
For reproducibility of the simulations or the conduct of new simulations on a local device (i.e., without HPC), the following codes from the ./example/code folder can be used:
- ```process_datasets.ipynb```
- ```simulate_datasets.py```
- ```processs_example_results.ipynb```

More detailed discription on how to use these codes for reproducibility or new simulations can be found in the README.md file in the ./example/ folder.

### Envs (conda environments)
The following environments were used on the HPC:
- ```SR_environment.yml```
- ```SR_environment_no-builds.yml```

The following environments were used on a local device (to process results and to run the example)
- ```simulations_env.yml```
- ```simulations_env_no_builds.yml```


### Data
The datasets of the intervention reviews (Table 1) were derived from the publicly available data of the [CLEF eHealth Task 2019](https://github.com/CLEF-TAR/tar/tree/master/2019-TAR) and can be retrieved from their repository by manually downloading them or automatically by using the data_processing.ipynb in the example/code/ folder. 
<br>
##### Table 1 | The datasets of previously conducted **prognosis reviews** that were used in the simulations

| Review ID | Review number | Total records    | Relevant records (%)    | Final inclusions | Reference | Title |
| --- | :---:   | :---: | :---: | :---: | :---: | :---: |
| Prog_reporting | 1 | 9160   | 54 (0.6)   | 25 | Andaur Navarro *et al.* (2022) | Completeness of reporting of clinical prediction models developed using supervised machine learning: a systematic review|
| Prog_cardio | 2 | 12319   | 88 (0.7)   | 81 | Damen *et al.* (2019) | Performance of the Framingham risk models and pooled cohort equations for predicting 10-year risk of cardiovascular disease: a systematic review and meta-analysis|
| Prog_tripod | 3 | 2815   | 37 (1.3)   | 10 | Heus *et al.* (2018) | Poor reporting of multivariable prediction model studies: towards a targeted implementation strategy of the TRIPOD statement|
| Prog_ecmo | 4 | 3874   | 52 (1.3)   | 12 | Pladet *et al.* (2023) | Prognostic models for mortality risk in patients requiring ECMO|
| Prog_ntcp | 5 | 8867   | 23 (0.3)   | 9 | Takada *et al.* (submitted) | Prognostic models for radiation‐induced complications after radiotherapy in head and neck cancer patients|
| Prog_rcri | 6 | 5392   | 112 (2.1)   | 68 | Vernooij *et al.* (2021) | The comparative and added prognostic value of biomarkers to the Revised Cardiac Risk Index for preoperative prediction of major adverse cardiac events and all-cause mortality in patients who undergo noncardiac surgery|

##### Table 2 | The datasets of previously conducted **intervention reviews** that were used in the simulations

| Review ID | Review number | Total records    | Relevant records (%)    | Final inclusions | Reference | Title |
| --- | :---:   | :---: | :---: | :---: | :---: | :---: |
| Int_CD011768 | 1 | 9160   | 54 (0.6)   | 25 | Arikpo *et al.* (2018) | Educational interventions for improving primary caregiver complementary feeding practices for children aged 24 months and under|
| Int_CD008170 | 2 | 12319   | 88 (0.7)   | 81 | Chen *et al.* (2018) | First‐line drugs inhibiting the renin angiotensin system versus other first‐line antihypertensive drug classes for hypertension|
| Int_CD010558 | 3 | 2815   | 37 (1.3)   | 10 | Ijaz *et al.* (2018) | Psychological therapies for treatment‐resistant depression in adults|
| Int_CD006468 | 4 | 3874   | 52 (1.3)   | 12 | Kahale *et al.* (2018) | Anticoagulation for people with cancer and central venous catheters|
| Int_CD010038 | 5 | 8867   | 23 (0.3)   | 9 | Kaufman *et al.* (2018) | Face‐to‐face interventions for informing or educating parents about early childhood vaccination|
| Int_CD005139 | 6 | 5392   | 112 (2.1)   | 68 | Solomon *et al.* (2019) | Anti‐vascular endothelial growth factor for neovascular age‐related macular degeneration|
| Int_CD008201 | 7 (A1) | 3574   | 11 (0.3)   | 8 | Kahn *et al.* (2019) | Interventions for implementation of thromboprophylaxis in hospitalized patients at risk for venous thromboembolism|
