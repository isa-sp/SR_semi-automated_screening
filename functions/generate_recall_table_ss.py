import numpy as np
import pandas as pd

def generate_recall_table_ss(evaluation, sample_sizes, n_simulations):
    
    length_ss = len(sample_sizes) * n_simulations

    df_ss = pd.DataFrame()
    for key, value in evaluation.items():
        print(key)
        names = key.split('_')
        review = [names[0]] * length_ss
        train_model = [names[1]] * length_ss
        feature_model = [names[2]] * length_ss
        query_model = [names[3]] * length_ss
        simulations = [] 

        nums = sample_sizes * n_simulations
        for i in range(1, n_simulations+1):
            simulations.append(list(np.repeat(i, len(sample_sizes))))
        recalls = value[0][1]['Recall']
        sim_number = value[0][1]['Simulation']

        simulations = [item for sublist in simulations for item in sublist]

        df_sim = pd.DataFrame(list(zip(review, train_model, feature_model, query_model, simulations, nums, recalls, sim_number)),
                              columns = ['Review', 'Train model', 'Feature model', 'Query model', 'Simulation', 'Number of records screened','Recall', 'Simulation number'])
        df_ss = pd.concat([df_ss, df_sim])

        df_ss = df_ss.reset_index(drop = True)

        df_ss['Simulation'] = ""
        for row in range(0, len(df_ss)):
              df_ss['Simulation'][row] = "Review " + str(df_ss['Review'][row]) + " (" + str(df_ss['Train model'][row]) + " - " + str(df_ss['Feature model'][row]) + " - " + str(df_ss['Query model'][row]) + ")"

    df_ss['Review_full'] = ""

    df_ss['Review_full'] = df_ss['Review'].apply(lambda x: x.replace("Prog", "Prognosis "))
    for i in range(0, len(df_ss['Review_full'])):
        if "Int" in df_ss['Review_full'][i]:
            df_ss['Review_full'][i] = df_ss['Review_full'][i].replace("Int", "Intervention ")

    df_ss['Simulation'] = ""
    for row in range(0, len(df_ss)):
          df_ss['Simulation'][row] = str(df_ss['Review_full'][row]) + " (" + str(df_ss['Train model'][row]) + " - " + str(df_ss['Feature model'][row]) + ")" 

    df_ss['Models'] = ""
    for row in range(0, len(df_ss)):
          df_ss['Models'][row] = str(df_ss['Train model'][row]) + " - " + str(df_ss['Feature model'][row])

    return df_ss  
