
import numpy as np
import pandas as pd

def compute_nwss(simulations, proportions, sample_sizes, n_prior_included = 10, n_prior_excluded = 10):
    
    '''
    simulations (list):        a list with each item being a unique review-model combination, and each such item being a dictionary 
                               that consists of rankings of each of the simulations of that review-model combination
    proportions (list):        a list of floats that represent proportions of screened records
                               at which to calculate the performance metrics
    sample_sizes (list):       a list of integers that represent sample sizes (number of screened records)
                               at which to calculate the performance metrics
    n_prior_included (int):    number of included (relevant) records that are used in the initial training set
                               -> Should be the same as was defined in the ASReview_simulation function
    n_prior_excluded (int):    number of excluded (irrelevant) records that are used in the initial training set
                               -> Should be the same as was defined in the ASReview_simulation function
    '''
    
    # Retrieve the size of the training set
    training_set_size = n_prior_included + n_prior_excluded
    # Create a list of proportions screened for calculation of the precision
    steps_prec = np.linspace(0.001, 0.999, 999,retstep = True)[0]
    
    output = []
    
    # For each unqiue review-model combination:
    for h in range(0, len(simulations)):

        # Retrieve the relevant components of the ASReview_simulation output (simulations)
        review_id = simulations[h][0]
        print(review_id)
        n_simulations = simulations[h][2]  
        simulation = simulations[h][3]
        sim = list(range(1,n_simulations+1))
 
        # Prepare the lists to store the outputs
        # List to store the recall at the specified sample size(s) of screened records
        recalls_ss =[]
        # List to store the normalized work saved over sampling at 95% recall (wss-95%)
        wss95_all = []
        nwss95 = []
        nwss95_2 = []
        min_wss95_long = []
        max_wss95_long = []
        # List to store the precision at 95% recall (precisions = []) and the proportions screened at that value of precision (step = [])
        step = []

        # For each simulation of the review-model combination:
        for i in simulation:
            
            # Retrieve the dataset of the simulation's ranking and remove the trainingset
            df_orig = simulation[i][0]
            review_length = len(df_orig)
            df = df_orig[training_set_size:review_length]
            
            n_inclusions = sum(df_orig['label'])  ##sum(df['label'])
            n_exclusions = review_length - n_inclusions
            max_wss95 = ((n_exclusions + (n_inclusions * (1-0.95))) / review_length) - (1-0.95) ##((n_exclusions + round((n_inclusions * (1-0.95)))) / review_length) - (1-0.95)
            min_wss95 = ((0 + (n_inclusions * (1-0.95))) / review_length) - (1-0.95) ##((0 + round((n_inclusions * (1-0.95)))) / review_length) - (1-0.95)
        
            recs_ss = []

            # To derive the recall at the specified sample size(s) of screened records
            for j in sample_sizes:
                
                # Check if the review length is longer than the number of records screened (sample size),
                # in order to continue the calculations
                if j <= review_length:
                    
                    # Use the number of records screened as the cutoff
                    cutoff = j
                    # Derive the labels before and after that cutoff
                    labels_at_samplesize = df['label'][0:cutoff]
                    labels_after_samplesize = df['label'][cutoff:]
                    
                    # Calculate the true positives (TP) as the number of positive labels before the cutoff
                    TP_at_samplesize = sum(labels_at_samplesize)
                    # Calculate the false negatives (FN) as the number of positive labels after the cutoff
                    FN_at_samplesize = sum(labels_after_samplesize)
                    # Calculate the recall based on the TP and FN
                    rec_at_samplesize = round((TP_at_samplesize / (TP_at_samplesize + FN_at_samplesize)), 2)
                    
                    recs_ss.append(rec_at_samplesize)
                
                # If the sample size is not possible for the respective review, fill 'NaN' in the output
                if j > review_length:
                    recs_ss.append(np.nan)
                    
            recalls_ss.append(recs_ss)

            # To derive the normalized work saved over sampling at 95% recall
            
            # Calculate the recall at increasing small steps of proportions screened, until a recall of 95% is found
            for k in range(0, len(steps_prec)):
                cutoff = round(float(steps_prec[k]*review_length))
                labels_at_step = df['label'][0:cutoff]
                labels_after_step = df['label'][cutoff:]

                TP_at_step = sum(labels_at_step)
                FN_at_step = sum(labels_after_step)
                FP_at_step = len(labels_at_step) - TP_at_step
                TN_at_step = len(labels_after_step) - FN_at_step

                rec = TP_at_step / (TP_at_step + FN_at_step)
                        
                # When the proportion of screened records at which recall is 95% is found,
                # store the proportion and calculate the wss@95%
                if rec >= 0.95:
                    step.append(steps_prec[k])
                    wss95 = (((review_length - cutoff) / review_length) - 0.05) # Used to be: (1-steps_prec[k]) 
                    nwss95.append(TN_at_step / (TN_at_step + FP_at_step)) 
                    nwss95_2.append((wss95 - min_wss95) / (max_wss95 - min_wss95))
                    wss95_all.append(wss95)
                    min_wss95_long.append(min_wss95)
                    max_wss95_long.append(max_wss95)
                    
                    break
            
        # Create a data frame with the WSS at 0.95 recall
        df_nwss = pd.DataFrame({'Simulation' : sim,
                                'WSS' : wss95_all, 
                                'minWSS-95%' : min_wss95_long,
                                'maxWSS-95%' : max_wss95_long,
                                'nWSS-95%' : nwss95,
                                'nWSS-95% 2' : nwss95_2,
                               })
        
        output.append((review_id, review_length, n_simulations, df_nwss))
        
    return output
 
