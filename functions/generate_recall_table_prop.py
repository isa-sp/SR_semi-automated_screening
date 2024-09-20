import numpy as np
import pandas as pd

def generate_recall_table_prop(evaluation, props, n_simulations):

    proportions = []
    for i in range(0, len(props)):
        proportions.append(str(int(props[i]*100)) + '%')
    length_prop = len(proportions) * n_simulations
    df_prop = pd.DataFrame()
    for key, value in evaluation.items():
        names = key.split('_')
        review = [names[0]] * length_prop
        train_model = [names[1]] * length_prop
        feature_model = [names[2]] * length_prop
        query_model = [names[3]] * length_prop
        simulations = []

        props = proportions * n_simulations
        for i in range(1, n_simulations+1):
            simulations.append(list(np.repeat(i, len(proportions))))
        recalls = value[0][0]['Recall']
        sim_number = value[0][0]['Simulation']

        simulations = [item for sublist in simulations for item in sublist]

        df_sim = pd.DataFrame(list(zip(review, sim_number, train_model, feature_model, query_model, simulations, props, recalls)),columns = ['Review', 'Simulation number', 'Train model', 'Feature model', 'Query model', 'Simulation', 'percentage of records screened','recall'])
        df_prop = pd.concat([df_prop, df_sim])

    df_prop = df_prop.reset_index(drop = True)

    df_prop['Review_full'] = ""

    df_prop['Review_full'] = df_prop['Review'].apply(lambda x: x.replace("Prog", "Prognosis "))
    for i in range(0, len(df_prop['Review_full'])):
        if "Int" in df_prop['Review_full'][i]:
            df_prop['Review_full'][i] = df_prop['Review_full'][i].replace("Int", "Intervention ")

    df_prop['Simulation'] = ""
    for row in range(0, len(df_prop)):
          df_prop['Simulation'][row] = str(df_prop['Review_full'][row]) + " (" + str(df_prop['Train model'][row]) + " - " + str(df_prop['Feature model'][row]) + ")" 

    df_prop['Models'] = ""
    for row in range(0, len(df_prop)):
          df_prop['Models'][row] = str(df_prop['Feature model'][row]) + " - " + str(df_prop['Train model'][row]) #+ " - " + str(df_prop['Feature model'][row])

    return df_prop
