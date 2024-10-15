# Semi-automated screening simulations for systematic reviews of prognosis and intervention studies

### Description
This repository contains the code of a simulation study on semi-automated title-abstract screening for systematic reviews of prognosis and intervention studies using the [ASReview](https://github.com/asreview) tool. The manuscript corresponding to the current study is in the process of submission:

**I. Spiero, A.M. Leeuwenberg, K.G.M. Moons, L. Hooft, J.A.A. Damen (2024). Evaluation of semi-automated record screening methods for systematic reviews of prognosis studies and intervention studies.** ___In submission___

### Python codes
The simulations were run in parallel on a High Performance Computer:
- simulate_original_datasets.py
- simulate_adapted_datasets.py
  
The derived output could be processed locally:
- process_results.ipynb

### Data
The datasets of the intervention reviews (Table 1) were derived from the publicly available data of the [CLEF eHealth Task 2019](https://github.com/CLEF-TAR/tar/tree/master/2019-TAR) and can be found in the data folder of this repository.

##### Table 1 | The datasets of previously conducted **intervention reviews** that were used in the simulation

| Review ID | Review number | Total records    | Relevant records (%)    | Final inclusions | Reference | Title |
| --- | :---:   | :---: | :---: | :---: | :---: | :---: |
| Int1_CD011768 | 1 | 9160   | 54 (0.6)   | 25 | Arikpo *et al.* (2018) | Educational interventions for improving primary caregiver complementary feeding practices for children aged 24 months and under|
| Int2_CD008170 | 2 | 12319   | 88 (0.7)   | 81 | Chen *et al.* (2018) | First‐line drugs inhibiting the renin angiotensin system versus other first‐line antihypertensive drug classes for hypertension|
| Int3_CD010558 | 3 | 2815   | 37 (1.3)   | 10 | Ijaz *et al.* (2018) | Psychological therapies for treatment‐resistant depression in adults|
| Int4_CD006468 | 4 | 3874   | 52 (1.3)   | 12 | Kahale *et al.* (2018) | Anticoagulation for people with cancer and central venous catheters|
| Int5_CD010038 | 5 | 8867   | 23 (0.3)   | 9 | Kaufman *et al.* (2018) | Face‐to‐face interventions for informing or educating parents about early childhood vaccination|
| Int6_CD005139 | 6 | 5392   | 112 (2.1)   | 68 | Solomon *et al.* (2019) | Anti‐vascular endothelial growth factor for neovascular age‐related macular degeneration|
| Int7_CD008201 | 7 (A1) | 3574   | 11 (0.3)   | 8 | Kahn *et al.* (2019) | Interventions for implementation of thromboprophylaxis in hospitalized patients at risk for venous thromboembolism|
