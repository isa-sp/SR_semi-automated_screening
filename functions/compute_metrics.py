
import numpy as np
import pandas as pd

def compute_metrics(simulations, proportions, sample_sizes, n_prior_included = 10, n_prior_excluded = 10):

    '''
    simulations (list):        a list with each item being a unique review-model combination, and each such item beingn a dictionary 
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
        # (1) Lists to store the recall, precision, specificity, and accuracy at the specified proportion(s) of screened records
        recalls_prop = []
        precisions_prop = []
        specificities_prop = []
        accuracies_prop = []
        # (2) List to store the recall at the specified sample size(s) of screened records
        recalls_ss =[]
        # (3) List to store the work saved over sampling at 95% recall (wss-95%)
        wss95 = []
        n_saved = [] ###
        # (4) List to store the precision at 95% recall (precisions = []) and the proportions screened at that value of precision (step = [])
        precisions = []
        step = []

        # For each simulation of the review-model combination:
        for i in simulation:
            
            # Retrieve the dataset of the simulation's ranking and remove the trainingset
            df_orig = simulation[i][0]
            review_length = len(df_orig)
            df = df_orig[training_set_size:review_length]

            recs = []
            precs = []
            specs = []
            accs = []
            recs_ss = []
            
            # (1) To derive the recall, precision, specificity, and accuracy at the specified proportion(s) of screened records
            for a in range(0, len(proportions)):
                if proportions[a] == 0:
                    recs.append(0)
                    precs.append(0)
                    specs.append(0)
                    accs.append(0)

                else:
                    # Calculate the cutoff: the number of records screened at the respective proportion
                    cutoff = round(float(proportions[a]*review_length))
                    # Derive the labels before and after that cutoff
                    labels_at_step = df['label'][0:cutoff]
                    labels_after_step = df['label'][cutoff:]

                    # Calculate the true positives (TP) as the number of positive labels before the cutoff
                    TP_at_step = sum(labels_at_step)
                    # Calculate the false positives (FP) as the number of negative labels before the cutoff
                    FP_at_step = len(labels_at_step) - TP_at_step
                    # Calculate the false negatives (FN) as the number of positive labels after the cutoff
                    FN_at_step = sum(labels_after_step)
                    # Calculate the true negatives (TN) as the number of negative labels after the cutoff
                    TN_at_step = len(labels_after_step) - FN_at_step

                    # Use the TP, FP, FN, and TN to calculate the recall, precision, specificity, and accuracy
                    rec = TP_at_step / (TP_at_step + FN_at_step)
                    prec = TP_at_step / (TP_at_step + FP_at_step)
                    spec = TN_at_step / (TN_at_step + FP_at_step)
                    acc = (TP_at_step + TN_at_step) / (TP_at_step + FP_at_step + FN_at_step + TN_at_step)

                    recs.append(rec)
                    precs.append(prec)
                    specs.append(spec)
                    accs.append(acc)

            recalls_prop.append(recs)
            precisions_prop.append(precs)
            specificities_prop.append(specs)
            accuracies_prop.append(accs)

            # (2) To derive the recall at the specified sample size(s) of screened records
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

            # (3 & 4) To derive the work saved over sampling and precision at 95% recall
            
            # Calculate the recall at increasing small steps of proportions screened, until a recall of 95% is found
            for k in range(0, len(steps_prec)):
                cutoff = round(float(steps_prec[k]*review_length))
                labels_at_step = df['label'][0:cutoff]
                labels_after_step = df['label'][cutoff:]

                TP_at_step = sum(labels_at_step)
                FN_at_step = sum(labels_after_step)
                
                #rec = round((TP_at_step / (TP_at_step + FN_at_step)), 2)
                rec = TP_at_step / (TP_at_step + FN_at_step)
                        
                # When the proportion of screened records at which recall is 95% is found,
                # store the proportion and calculate the wss@95%
                if rec >= 0.95:
                    step.append(steps_prec[k])
                    wss95.append(((review_length-cutoff)/review_length) - 0.05) # Used to be: (1-steps_prec[k])
                    n_saved.append((review_length-cutoff))###
                    break
            
        # (1) Create data frame with the metrics at different proportions screened
        simulations_prop = list(np.repeat(sim, len(proportions)))
        props = [item for sublist in [proportions]*len(sim) for item in sublist]
        
        df_prop = pd.DataFrame({'Simulation' : simulations_prop,
                                'Proportion' : props,
                                'Recall' : [item for sublist in recalls_prop for item in sublist],
                                'Precision' : [item for sublist in precisions_prop for item in sublist],
                                'Specificity' : [item for sublist in specificities_prop for item in sublist],
                                'Accuracy' : [item for sublist in accuracies_prop for item in sublist],
                               }) 
        # (2) Create a data frame with the recall at different sample sizes screened
        simulations_ss = list(np.repeat(sim, len(sample_sizes)))
        ss = [item for sublist in [sample_sizes]*len(sim) for item in sublist]
        df_ss = pd.DataFrame({'Simulation' : simulations_ss,
                              'Sample size' : ss,
                              'Recall' : [item for sublist in recalls_ss for item in sublist]
                             }) 
        # (3) Create a data frame with the WSS at 0.95 recall
        df_wss = pd.DataFrame({'Simulation' : sim,
                               'WSS-95%' : wss95,
                             })
        df_n_saved = pd.DataFrame({'Simulation' : sim,
                                   'Workload reduction (records)' : n_saved,
                                  }) ###

        # (4) Create a data frame with the precision at 0.95 recall
        for l in range(0,len(step)):
            cutoff = round(float(step[l]*review_length))
            labels_at_step = df['label'][0:cutoff]
            labels_after_step = df['label'][cutoff:]
            TP_at_step = sum(labels_at_step)
            FP_at_step = len(labels_at_step) - TP_at_step
            FN_at_step = sum(labels_after_step)
            TN_at_step = len(labels_after_step) - FN_at_step
            prec = TP_at_step / (TP_at_step + FP_at_step)
            precisions.append(prec)
        df_prec = pd.DataFrame({'Simulation' : sim,
                                'Proportion screened' : step,
                                'Precision' : precisions,
                             })
        
        output.append((review_id, review_length, n_simulations, df_prop, df_ss, df_wss, df_n_saved, df_prec))
        
    return output

