import numpy as np
import pandas as pd
import pickle
import os
import shutil
import glob

# Do not forget to create the folders (by running mkdir -p /tmp/transformers_cache /tmp/torch_cache in the command line) before running this part:
os.environ['TRANSFORMERS_CACHE'] = '/tmp/transformers_cache'
os.environ['TORCH_HOME'] = '/tmp/torch_cache'

from pathlib import Path
from asreview import ASReviewData, ASReviewProject
from asreview.review import ReviewSimulate
from asreview.models.classifiers import LogisticClassifier, NaiveBayesClassifier, LSTMBaseClassifier, LSTMPoolClassifier, NN2LayerClassifier, RandomForestClassifier, SVMClassifier
from asreview.models.query import MaxQuery, ClusterQuery, MaxRandomQuery, MaxUncertaintyQuery, RandomQuery, UncertaintyQuery
from asreview.models.balance import DoubleBalance, SimpleBalance, UndersampleBalance
from asreview.models.feature_extraction import Doc2Vec, Tfidf, SBERT, EmbeddingIdf, EmbeddingLSTM
from asreview import open_state

# Load the data
def load_data(path_data):
    """
    Load all .xlsx files from a given folder into a dictionary of DataFrames.
    Cleans 'title' and 'abstract' columns by replacing NaNs with empty strings.

    Parameters:
        path_data (str): Path to the folder containing the .xlsx files.

    Returns:
        dict: A dictionary with keys from filenames and values as cleaned DataFrames.
    """
    xlsx_files = glob.glob(os.path.join(path_data, "*.csv"))
    review_dic = {}
    for file in xlsx_files:
        filename = os.path.basename(file)
        key = filename.split('.')[0]
        df = pd.read_csv(file)
        # Clean and convert title/abstract
        for col in ['title', 'abstract']:
            if col in df.columns:
                df[col] = df[col].replace(np.nan, '').astype(str)
        review_dic[key] = df
    return review_dic

# Create a path to store the simulation results
def create_path(path_results):
    os.chdir(path_results)
    path_name = "simulation_results_new_evaluation"
    project_path = Path(path_name)
    project_path.mkdir(exist_ok=True)
    return path_name

# Define the function for ranking simulation(s)
def ASReview_simulation(review_id, review_data, path_name,
                        train_model=NaiveBayesClassifier(),
                        query_model=MaxQuery(), balance_model=DoubleBalance(), feature_model=Tfidf(),
                        n_simulations=10, n_model_update=10, n_prior_included=10, n_prior_excluded=10):
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
        balance_model:                    balance method by which class imbalance is handled, being either:
                                               DoubleBalance(), SimpleBalance(), or UndersampleBalance()
                                               -> Default by ASReview is DoubleBalance()
        feature_model:                    feature model used to derive features from the title and abstract, being either:
                                               Doc2Vec(), EmbeddingIdf(), EmbeddingLSTM(), SBERT(), Tfidf()
                                               -> Default by ASReview is Tfidf()
        n_simulations (int):              number of complete simulations to perform, each time with a different initial training set
        n_prior_included (int):           number of included (relevant) records that are used in the initial training set
                                               -> Default by ASReview is 10
        n_prior_excluded (int):           number of excluded (irrelevant) records that are used in the initial training set
                                               -> Default by ASReview is 10
        n_model_update (int):             number of records of which the screening is simulated before the model is updated
                                               -> Default by ASReview is 10
    """
    # Create an id for the review based on name and models
    review_id = review_id + "_" + str(train_model.name) + "_" + str(feature_model.name) + "_" + str(query_model.name)

    # Derive the review length
    review_length = len(review_data)

    # Create an empty dictionary to store the rankings of the records of each simulation
    dict_rank = {}

    # Run the simulations
    for i in list(range(1, n_simulations + 1)):

        # Set the path for the temporary results
        project_path = Path(path_name)
        project_path.mkdir(exist_ok=True)

        # Run the simulation based on the settings and store the output at the project path
        print("Running simulation number", i)
        print("Models: ", feature_model, train_model)
        # (Derived from ASReview from here...
        reviewer = ReviewSimulate(
            init_seed=int(i),
            as_data=ASReviewData(review_data),
            model=train_model,
            query_model=query_model,
            balance_model=balance_model,
            feature_model=feature_model,
            n_instances=n_model_update,
            project=ASReviewProject.create(
                project_path=project_path / "{y}.{x}_simulation".format(x=i, y=review_id),
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

            # Derive the rankings of the records and store in the dictionary
            dict_rank[i] = []
            dict_rank[i].append(labeled)

        # Close and remove the simulation results from the path
        shutil.rmtree(project_path)

        # Save the simulation
        os.chdir("../" + path_results_HPC)

        with open('sim_{review}_{simu}.p'.format(review=review_id, simu=i), 'wb') as f:
            pickle.dump(dict_rank, f)

    # Return the relevant results of the simulations
    return review_id, review_length, n_simulations, dict_rank


# Test each different method (and interactions) with the following loop for Tfidf():
def run_simulations(path_name, review_dic, train_models, feature_models, query_models):
    sim_list = []
    multiple_sims_saved = []
    for review in review_dic:
        for train_model in train_models:
            for feature_model in feature_models:
                for query_model in query_models:

                    # Cannot run incompatible models, therefore skip those:
                    # Skip NaiveBayes + Doc2Vec combo
                    if isinstance(train_model, NaiveBayesClassifier) and isinstance(feature_model, Doc2Vec):
                        print("NaiveBayesClassifier and Doc2Vec are not compatible.\nSimulation skipped.")
                        continue
                    # Skip NaiveBayes + SBERT combo
                    if isinstance(train_model, NaiveBayesClassifier) and isinstance(feature_model, SBERT):
                        print("NaiveBayesClassifier and SBERT are not compatible.\nSimulation skipped.")
                        continue

                    # SBERT likely only runs smoothly on High Performance Computers:
                    if isinstance(feature_model, SBERT):
                        while True:
                            answer = input(
                                f"The current feature extraction model SBERT may not run on a local device. Do you want to skip this simulation? (y/n): ").strip().lower()
                            if answer == 'y':
                                print("Skipping the simulation with feature extraction model SBERT.")
                                break
                            elif answer == 'n':
                                print("Trying to run the simulation with feature extraction model SBERT...")
                                break
                            else:
                                print("Please answer either 'y' or 'n'.")

                        if answer == 'y':
                            continue

                    sim_list.append([review, train_model, feature_model, query_model])
                    sim = ASReview_simulation(review_id = review, review_data = review_dic[review],
                                              path_name = path_name,
                                              train_model = train_model, query_model = query_model,
                                              balance_model = DoubleBalance(), feature_model = feature_model,
                                              n_simulations = 10, n_model_update = 10,
                                              n_prior_included = 10, n_prior_excluded = 10)
                    multiple_sims_saved.append(sim)

if __name__ == "__main__":
    # Define the paths
    path_data = "../data/processed/"
    path_results = '../output/tmp/'
    path_results_HPC = '../output/rankings'

    # Define the model(s) to be tested
    train_models = [LogisticClassifier(), NaiveBayesClassifier()] #[LogisticClassifier(), NaiveBayesClassifier(), SVMClassifier()]
    feature_models = [Tfidf()] #[Tfidf(), SBERT()]
    query_models = [MaxQuery()]

    # Run the simulations
    review_dic = load_data(path_data)
    path_name = create_path(path_results)
    run_simulations(path_name, review_dic, train_models, feature_models, query_models)
