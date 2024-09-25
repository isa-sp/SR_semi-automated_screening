# Import the packages

import numpy as np
import pandas as pd
import pickle
import os
import shutil
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Running simulations in  parallel')
parser.add_argument('-sim_id', type=int, default=1, help='Number')
args = parser.parse_args()

path_data = '/home/julius_te/ispiero/systematicreviews/data/data_HPC' #'/Users/ispiero2/Documents/Research/Datasets/Systematic_reviews/Datasets_final/Clean_datasets/' 
path_results = '/hpc/local/Rocky8/julius_te/ispiero/SR_results/new_results' #'/home/julius_te/ispiero/systematicreviews/results' #'/Users/ispiero2/Documents/Research/Results_tmp/'

###

# Import the intervention review datasets (numbering of the datasets is ordered by authors)

os.chdir(path_data)

# Intervention dataset 1: CD011768 - Educational interventions for improving primary caregiver complementary feeding practices for children aged 24 months and under
df_int1 = pd.read_excel('Int_CD011768_labeled.xlsx')

# Intervention dataset 2: CD008170 - First‐line drugs inhibiting the renin angiotensin system versus other first‐line antihypertensive drug classes for hypertension
df_int2 = pd.read_excel('Int_CD008170_labeled.xlsx')

# Intervention dataset 3: CD010558 - Psychological therapies for treatment‐resistant depression in adults
df_int3 = pd.read_excel('Int_CD010558_labeled.xlsx')

# Intervention dataset 4: CD006468 - Anticoagulation for people with cancer and central venous catheters
df_int4 = pd.read_excel('Int_CD006468_labeled.xlsx')

# Intervention dataset 5: CD010038 - Face‐to‐face interventions for informing or educating parents about early childhood vaccination
df_int5 = pd.read_excel('Int_CD010038_labeled.xlsx')

# Intervention dataset 6: CD005139 - Anti‐vascular endothelial growth factor for neovascular age‐related macular degeneration
df_int6 = pd.read_excel('Int_CD005139_labeled.xlsx')

# Intervention dataset 7: CD012069 - Methylphenidate for attention deficit hyperactivity disorder (ADHD) in children and adolescents – assessment of adverse events in non‐randomised studies
df_int7 = pd.read_excel('Int_CD012069_labeled.xlsx')


# Intervention dataset Appendix1: CD008201 - Interventions for implementation of thromboprophylaxis in hospitalized patients at risk for venous thromboembolism
df_int8 = pd.read_excel('Int_CD008201_labeled.xlsx')

# Intervention dataset Appendix2: CD012342 - Comparison of a therapeutic‐only versus prophylactic platelet transfusion policy for people with congenital or acquired bone marrow failure disorders
df_int9 = pd.read_excel('Int_CD012342_labeled.xlsx')

###

# Import the prognosis datasets (numbering of the datasets is ordered by author, so numbers do not correspond to numbers in data prep)

os.chdir(path_data)

# Prognosis dataset 1: model reporting
df_prog1 = pd.read_excel('Prog_reporting_labeled.xlsx')

# Prognosis dataset 2: cardiovascular risk
df_prog2 = pd.read_excel('Prog_cardio_labeled.xlsx')

# Prognosis dataset 3: tripod
df_prog3 = pd.read_excel('Prog_tripod_labeled.xlsx')

# Prognosis dataset 4: ecmo
df_prog4 = pd.read_excel('Prog_ecmo_labeled.xlsx')

# Prognosis dataset 5: diabetes
df_prog5 = pd.read_excel('Prog_diabetes_labeled.xlsx')

# Prognosis dataset 6: ntcp
df_prog6 = pd.read_excel('Prog_ntcp_labeled.xlsx')

# Prognosis dataset 7: rcri
df_prog7 = pd.read_excel('Prog_rcri_labeled.xlsx')

###

# Create dictionaries of the datasets

dfs_int = {'Int1' : df_int1,
           'Int2' : df_int2,
           'Int3' : df_int3,
           'Int4' : df_int4,
           'Int5' : df_int5,
           'Int6' : df_int6,
           'Int7' : df_int7,
           'Int8' : df_int8,
           'Int9' : df_int9
          }

dfs_prog = {'Prog1' : df_prog1,
            'Prog2' : df_prog2,
            'Prog3' : df_prog3,
            'Prog4' : df_prog4,
            'Prog5' : df_prog5,
            'Prog6' : df_prog6,
            'Prog7' : df_prog7
          }

###

# Change the titles and abstracts into the correct data type

for review in dfs_int:
    dfs_int[review]['title'] = dfs_int[review]['title'].replace(np.nan, '')
    dfs_int[review]['abstract'] = dfs_int[review]['abstract'].replace(np.nan, '')
    dfs_int[review]['title'] = dfs_int[review]['title'].astype(str)
    dfs_int[review]['abstract'] = dfs_int[review]['abstract'].astype(str)

for review in dfs_prog:
    dfs_prog[review]['title'] = dfs_prog[review]['title'].replace(np.nan, '')
    dfs_prog[review]['abstract'] = dfs_prog[review]['abstract'].replace(np.nan, '')
    dfs_prog[review]['title'] = dfs_prog[review]['title'].astype(str)
    dfs_prog[review]['abstract'] = dfs_prog[review]['abstract'].astype(str)

###

# Create a path to store the simulation results

os.chdir(path_results)

from pathlib import Path
from asreview import ASReviewData, ASReviewProject
from asreview.review import ReviewSimulate

path_name = "simulation_results_new_evaluation"
#project_path = Path(path_name)
#project_path.mkdir(exist_ok = True)

###

# Define the function for ASReview simulation(s)

# Import the functions from ASReview
# Classifiers:
from asreview.models.classifiers import LogisticClassifier, LSTMBaseClassifier, LSTMPoolClassifier, \
    NaiveBayesClassifier, NN2LayerClassifier, RandomForestClassifier, SVMClassifier

# Query models:
from asreview.models.query import ClusterQuery, MaxQuery, MaxRandomQuery, MaxUncertaintyQuery, RandomQuery, \
    UncertaintyQuery

# Balance models:
from asreview.models.balance import DoubleBalance, SimpleBalance, UndersampleBalance

# Feature extraction models:
from asreview.models.feature_extraction import Doc2Vec, EmbeddingIdf, EmbeddingLSTM, SBERT, Tfidf

# For evaluation:
from asreview import open_state


def ASReview_simulation(review_id, review_data, path_name, 
                        sim_id, 
                        train_model=NaiveBayesClassifier(),
                        query_model=MaxQuery(), balance_model=DoubleBalance(), feature_model=Tfidf(),
                       # n_simulations=10,
                        n_model_update=10, n_prior_included=10, n_prior_excluded=10):
    """
        Performs semi-automated title-abstract screening simulations
        based on a labeled review dataset using the open source codes of ASReview.

        review_id (str):                  name under which the user wants to save the output for the respective review
        review_data (pandas.DataFrame):   dataframe containing at least columns with the 'title', 'abstract', and 'label_included'
        path_name (str):                  name of the path at which the simulation results are stored temporarily in each iteration
        train_model:                      classification model used to classify (rank) the records for relevance, being either:
                                               LogisticClassifier(), LSTMBaseClassifier(), LSTMPoolClassifier(), NaiveBayesClassifier(),
                                               NN2LayerClassifier(), RandomForestClassifier(), or SVMClassifier()
                                               -> Default by ASReview is NaiveBayesClassifier()
        query_model:                      query method by which the screener is presented with records, being either:
                                               ClusterQuery(), MaxQuery(), MaxRandomQuery(), MaxUncertaintyQuery(), RandomQuery(), or UncertaintyQuery()
                                               -> Default by ASReview is MaxQuery()
        balance_model:                    ...., being either:
                                               DoubleBalance(), SimpleBalance(), or UndersampleBalance()
                                               -> Default by ASReview is DoubleBalance()
        feature_model:                    feature model used to derive features from the title and abstract, being either:
                                               TDoc2Vec(), EmbeddingIdf(), EmbeddingLSTM(), SBERT(), Tfidf()
                                               -> Default by ASReview is Tfidf()
        n_simulations (int):              number of complete simulations to perform, each time with a different initial training set
        n_prior_included (int):           number of included (relevant) records that are used in the initial training set
                                               -> Default by ASReview is 10
        n_prior_excluded (int):           number of excluded (irrelevant) records that are used in the initial training set
                                               -> Default by ASReview is 10
        n_model_update (int):             number of records of which the screening is simulated before the model is updated
                                               -> Default by ASReview is 10
    """

    # Create a list of numbers ranging from 1 to n_simulations
    sim = sim_id  #list(range(1, n_simulations + 1))

    # Create an id for the review based on name and models
    review_id = review_id + "_" + str(train_model.name) + "_" + str(feature_model.name) + "_" + str(query_model.name)

    # Derive the review length
    review_length = len(review_data)

    # Create an empty dictionary to store the rankings of the records of each simulation
    dict_rank = {}

    # Run the simulations
    #for i in sim:

    # Set the path for the temporary results
    #path_name = path_name
    #project_path = Path(path_name)
    #project_path.mkdir(exist_ok=True)
    project_path = Path(path_name+"{y}.{x}_simulation".format(x=sim, y=review_id)) #{y}_simulation".format(y=review_id))#
    project_path.mkdir(exist_ok=True)

    # Run the simulation based on the settings and store the output at the project path
    print(sim)
    # (Derived from ASReview from here...
    reviewer = ReviewSimulate(
        init_seed=int(sim),  
        as_data=ASReviewData(review_data),
        model=train_model,
        query_model=query_model,
        balance_model=balance_model,
        feature_model=feature_model,
        n_instances=n_model_update,
        project=ASReviewProject.create(
            project_path=project_path/ "{y}.{x}_simulation".format(x=i, y=review_id),
            project_id="{y}.{x}".format(x=i, y=review_id),
            project_mode="simulate",
            project_name="{y}.{x}".format(x=i, y=review_id)
        ),
        n_prior_included=n_prior_included,
        n_prior_excluded=n_prior_excluded
    )
    reviewer.project.update_review(status="review")
    try:
        reviewer.review()
        reviewer.project.mark_review_finished()
    except Exception as err:
        reviewer.project.update_review(status="error")
        raise err
    # ...until here)

    # Open the stored simulation results
    with open_state(reviewer.project) as s:
        labeled = s.get_labeled()
        priors = s.get_priors()
        labels = labeled[~labeled['record_id'].isin(priors['record_id'])]

        # Derive the rankings of the records and store in the dictionary
        dict_rank[sim] = []
        dict_rank[sim].append(labeled)

    # Close and remove the simulation results from the path
    shutil.rmtree(project_path)

    # Save the simulation
    os.chdir(path_results)

    with open('sim_{review}_{simu}.p'.format(review=review_id, simu = sim),'wb') as f:
        pickle.dump(dict_rank,f)

    # Return the relevant results of the simulations
    return review_id, review_length, dict_rank #n_simulations, dict_rank


# A test run to test the function
# test_simulation = ASReview_simulation(review_id='Prog1', review_data=dfs_prog['Prog1'], path_name=path_name,
#                                       train_model=NaiveBayesClassifier(), query_model=MaxQuery(),
#                                       balance_model=DoubleBalance(), feature_model=Tfidf(),
#                                       n_simulations=10,  
#                                       n_model_update=10, n_prior_included=10, n_prior_excluded=10)

###

# To assess the performance of ASReview, the reviews, the classification models,
# feature extraction models, and/or query models are varied.

# Create/use a dictionary with the datasets of labeled reviews as values
#review_dic = {#'Prog1' : dfs_prog['Prog1']#,
              #'Prog2' : dfs_prog['Prog2'],
              #'Prog3' : dfs_prog['Prog3'],
              #'Prog4' : dfs_prog['Prog4'],
              #'Prog5' : dfs_prog['Prog5'],
              #'Prog6' : dfs_prog['Prog6'],
              #'Prog7' : dfs_prog['Prog7'],
              #'Int1' : dfs_int['Int1'],
              #'Int2' : dfs_int['Int2'],
              #'Int3' : dfs_int['Int3'],
              #'Int4' : dfs_int['Int4'],
              #'Int5' : dfs_int['Int5'],
              #'Int6' : dfs_int['Int6'],
              #'Int7' : dfs_int['Int7'],
              #'Int8' : dfs_int['Int8']#,
             #'Int9' : dfs_int['Int9']
         #}
# Define a function to create a dictionary with subsets of a dataset consisting of varying numbers of records and inclusions:

def df_var_dict(review_name, df, sizes, incl_prop):
    '''
    df (pandas.DataFrame):    a dataframe of a review with at least containing the columns 'abstract', 'title', and 'label_included'
    sizes (list):             a list of integers of dataframe sizes to vary
    incl_prop (list):         a list of integers of inclusion proportions to vary
    '''

    # First a list of possible size/inclusion combinations is created:
    unique_combinations = []
    for i in range(0, len(sizes)):
        unique_combinations.append([sizes[i], incl_prop[i]])

    # Then a dictionary is created with for each combination a sample of the dataset. If the sample cannot be retrieved,
    # i.e. the dataset size is too small or the inclusion proportion is not available, the respective item in the dictionary remains empty.
    df_dict = {}

    # For each combination of size/inclusion proportion:
    for i in range(len(unique_combinations)):
        # Check if the dataframe includes enough records to sample the respective size
        if len(df) >= unique_combinations[i][0]:

            # Check if the inclusion proportion is possible for the respective size
            if df.loc[df['label_included'] == 1].shape[0] >= int(
                    unique_combinations[i][0] * unique_combinations[i][1]) and df.loc[df['label_included'] == 0].shape[
                0] >= int(unique_combinations[i][0] - (unique_combinations[i][0] * unique_combinations[i][1])):
                # If so:
                # Sample random inclusions
                incl = df.loc[df['label_included'] == 1].sample(
                    n=int(unique_combinations[i][0] * unique_combinations[i][1]), replace=False, random_state=1)
                # Sample random exclusions
                excl = df.loc[df['label_included'] == 0].sample(
                    n=int(unique_combinations[i][0] - (unique_combinations[i][0] * unique_combinations[i][1])),
                    replace=False, random_state=1)
                # Create a dataframe of the inclusions and exclusions
                df_new = pd.concat([incl, excl]).sort_values('authors').reset_index()
                name = review_name + "_" + str(len(df_new)) + "_" + str(unique_combinations[i][1])
            # If the size/inclusion proportion is not possible, leave the dataframe empty
            else:
                name = review_name + "_" + str(len(df_new)) + "_" + str(unique_combinations[i][1])
                df_new = []
        else:
            df_new = []

        if len(df_new) > 0:
            if df_new['label_included'].sum() <= 10:
                df_new = []

        # Store the dataframe in the dictionary of all retrieved dataframes
        if len(df_new) > 0:
            df_dict[name] = df_new

    return (df_dict)

# Apply the function:
sizes = [500, 1000, 2000]
incl_prop = [0.1, 0.05, 0.025]
ss_dict = df_var_dict(review_name = 'Int1', df = dfs_int['Int1'], sizes = sizes, incl_prop = incl_prop)
ss_dict.update(df_var_dict(review_name = 'Int2', df = dfs_int['Int2'], sizes = sizes, incl_prop = incl_prop))
ss_dict.update(df_var_dict(review_name = 'Int4', df = dfs_int['Int4'], sizes = sizes, incl_prop = incl_prop))
ss_dict.update(df_var_dict(review_name = 'Int6', df = dfs_int['Int6'], sizes = sizes, incl_prop = incl_prop))
ss_dict.update(df_var_dict(review_name = 'Prog3', df = dfs_prog['Prog3'], sizes = sizes, incl_prop = incl_prop))
ss_dict.update(df_var_dict(review_name = 'Prog4', df = dfs_prog['Prog4'], sizes = sizes, incl_prop = incl_prop))
ss_dict.update(df_var_dict(review_name = 'Prog6', df = dfs_prog['Prog6'], sizes = sizes, incl_prop = incl_prop))
ss_dict.update(df_var_dict(review_name = 'Prog7', df = dfs_prog['Prog7'], sizes = sizes, incl_prop = incl_prop))

#ss_dict.keys()
review_dic = ss_dict

# Define the classification model(s) to be tested
train_models = [NaiveBayesClassifier()] #[LogisticClassifier(), NaiveBayesClassifier(), SVMClassifier()]

# Define the feature extraction model(s) to be tested
feature_models = [Tfidf()] #[Tfidf(), SBERT()] # SBERT() only works with PyCharm

# Define the query model(s) to be tested (for now no variation in query models)
query_models = [MaxQuery()]

###

# Test each different method (and interactions) with the following loop for Tfidf():

sim_list = []
sim_list_names = []
multiple_sims_saved = []
for review in review_dic:
    for train_model in train_models:
        for feature_model in feature_models:
            for query_model in query_models:
                sim_list.append([review, train_model, feature_model, query_model])
                sim_list_names.append(str(review + "_" + train_model.name + "_" + feature_model.name + "_" + query_model.name))
                # sim = ASReview_simulation(review_id = review, review_data = review_dic[review],
                #                           path_name = path_name,
                #                           train_model = train_model, query_model = query_model,
                #                           balance_model = DoubleBalance(), feature_model = feature_model,
                #                           n_simulations = 10, n_model_update = 10,
                #                           n_prior_included = 10, n_prior_excluded = 10)
                # multiple_sims_saved.append(sim)

###

# Test each different method (and interactions) with the following loop for SBERT():

# feature_models = [SBERT()]
# train_models = [LogisticClassifier(), SVMClassifier()]

# sim_list = []
# multiple_sims_saved = []
# for review in review_dic:
#     for train_model in train_models:
#         for feature_model in feature_models:
#             for query_model in query_models:
#                 sim_list.append([review, train_model, feature_model, query_model])
#                 sim = ASReview_simulation(review_id = review, review_data = review_dic[review],
#                                           path_name = path_name,
#                                           train_model = train_model, query_model = query_model,
#                                           balance_model = DoubleBalance(), feature_model = feature_model,
#                                           n_simulations = 10, n_model_update = 10,
#                                           n_prior_included = 10, n_prior_excluded = 10)
#                 multiple_sims_saved.append(sim)

###

# On the HPC:

for i in range(0, len(sim_list)):
    if Path(path_results +'sim_{review_id}_{sim}.p'.format(review_id=sim_list_names[i], sim=args.sim_id)).is_file():
        pass
    else:
        ASReview_simulation(review_id = sim_list[i][0],
                            review_data = review_dic[sim_list[i][0]],
                            path_name = path_name,
                            sim_id = args.sim_id,
                            train_model = sim_list[i][1],
                            query_model = sim_list[i][3],
                            balance_model = DoubleBalance(),
                            feature_model = sim_list[i][2],
                            #n_simulations = 1000,
                            n_model_update = 10,
                            n_prior_included = 10, n_prior_excluded = 10)

