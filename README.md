# Semi-automated screening simulations for systematic reviews of prognosis and intervention studies

**I. Spiero, A.M. Leeuwenberg, K.G.M. Moons, L. Hooft, J.A.A. Damen (2024). Evaluation and comparison of semi-automated record screening methods for systematic reviews of prognosis studies and intervention studies.** ___Submitted___

### Description
This repository contains the code of a simulation study on semi-automated title-abstract screening for systematic reviews of prognosis and intervention studies using the [ASReview](https://github.com/asreview) tool. The manuscript corresponding to the current study is submitted/under review for publication.

### Python codes
The simulations were run in parallel on a High Performance Computer:
- simulate_original_datasets.py
- simulate_adapted_datasets.py
  
The derived output could be processed locally:
- process_results.ipynb

### Data
The prognosis reviews (Table 1) are listed and may become available in the data folder upon approval of the respective authors. The intervention reviews (Table 2) are derived from the publicly available data of the [CLEF eHealth Task 2019](https://github.com/CLEF-TAR/tar/tree/master/2019-TAR) and can be found already in the data folder of this repository.

##### Table 1 | The datasets of previously conducted **prognosis reviews** that were used in the simulation

| Review ID | Review number | Total records    | Relevant records (%)    | Final inclusions | Authors | Title |
| --- | :---:   | :---: | :---: | :---: | :---: | :---: |
| Prog1_reporting | 1 | 2482   | 312 (12.6)   | 166 | Andaur Navarro *et al.* (2022) | Completeness of reporting of clinical prediction models developed using supervised machine learning: a systematic review|
| Prog2_cardio | 2 | 777   | 91 (11.7)   | 38 | Damen *et al.* (2019) | Performance of the Framingham risk models and pooled cohort equations for predicting 10-year risk of cardiovascular disease: a systematic review and meta-analysis|
| Prog3_tripod | 3 | 4871   | 347 (7.1)   | 146 | Heus *et al.* (2018) | Poor reporting of multivariable prediction model studies: towards a targeted implementation strategy of the TRIPOD statement|
| Prog4_ecmo | 4 | 4274   | 377 (8.8)   | 88 | Pladet *et al.* (2023) | Prognostic models for mortality risk in patients requiring ECMO|
| Prog5_ntcp | 5 | 10664   | 953 (8.9)   | 114 | Takada *et al.* (submitted) | Prognostic models for radiation‐induced complications after radiotherapy in head and neck cancer patients|
| Prog6_rcri | 6 | 3999   | 1064 (26.6)   | 107 | Vernooij *et al.* (2021) | The comparative and added prognostic value of biomarkers to the Revised Cardiac Risk Index for preoperative prediction of major adverse cardiac events and all-cause mortality in patients who undergo noncardiac surgery|


##### Table 2 | The datasets of previously conducted **intervention reviews** that were used in the simulation

| Review ID | Review number | Total records    | Relevant records (%)    | Final inclusions | Authors | Title |
| --- | :---:   | :---: | :---: | :---: | :---: | :---: |
| Int1_CD011768 | 1 | 9160   | 54 (0.6)   | 25 | Arikpo *et al.* (2018) | Educational interventions for improving primary caregiver complementary feeding practices for children aged 24 months and under|
| Int2_CD008170 | 2 | 12319   | 88 (0.7)   | 81 | Chen *et al.* (2018) | First‐line drugs inhibiting the renin angiotensin system versus other first‐line antihypertensive drug classes for hypertension|
| Int3_CD010558 | 3 | 2815   | 37 (1.3)   | 10 | Ijaz *et al.* (2018) | Psychological therapies for treatment‐resistant depression in adults|
| Int4_CD006468 | 4 | 3874   | 52 (1.3)   | 12 | Kahale *et al.* (2018) | Anticoagulation for people with cancer and central venous catheters|
| Int5_CD010038 | 5 | 8867   | 23 (0.3)   | 9 | Kaufman *et al.* (2018) | Face‐to‐face interventions for informing or educating parents about early childhood vaccination|
| Int6_CD005139 | 6 | 5392   | 112 (2.1)   | 68 | Solomon *et al.* (2019) | Anti‐vascular endothelial growth factor for neovascular age‐related macular degeneration|
| Int7_CD008201 | 7 (A1) | 3574   | 11 (0.3)   | 8 | Kahn *et al.* (2019) | Interventions for implementation of thromboprophylaxis in hospitalized patients at risk for venous thromboembolism|
