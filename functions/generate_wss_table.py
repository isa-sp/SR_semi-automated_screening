import pandas as pd

def generate_wss_table(evaluation, evaluation_nwss, n_simulations):

    df_wss = pd.DataFrame()
    length = n_simulations
    for key, value in evaluation.items():
        names = key.split('_')
        review = [names[0]] * length
        train_model = [names[1]] * length
        feature_model = [names[2]] * length
        query_model = [names[3]] * length
        simulations = range(1, n_simulations+1)
        wss = value[0][2]['WSS-95%']
        n_saved = value[0][3]['Workload reduction (records)'] ###
        df_sim = pd.DataFrame(list(zip(review, train_model, feature_model, query_model, simulations, wss, n_saved)),
                               columns = ['Review', 'Train model', 'Feature model', 'Query model', 'Simulation', 'WSS@95%', 'Workload reduction (n)'])
        df_wss = pd.concat([df_wss, df_sim])

        df_wss = df_wss.reset_index(drop = True)

    df_nwss = pd.DataFrame()
    length = n_simulations
    for key, value in evaluation_nwss.items():
        names = key.split('_')
        review = [names[0]] * length
        train_model = [names[1]] * length
        feature_model = [names[2]] * length
        query_model = [names[3]] * length
        simulations = range(1, n_simulations+1)
        nwss = value[0][0]['nWSS-95%']
        df_sim = pd.DataFrame(list(zip(review, train_model, feature_model, query_model, simulations, nwss)),
                               columns = ['Review', 'Train model', 'Feature model', 'Query model', 'Simulation', 'n-WSS@95%'])
        df_nwss = pd.concat([df_nwss, df_sim])

        df_nwss = df_nwss.reset_index(drop = True)

    df_wss = pd.merge(df_wss[['Review', 'Train model', 'Feature model', 'Query model', 'Simulation', 'WSS@95%', 'Workload reduction (n)']], 
                      df_nwss[['Review', 'Train model', 'Feature model', 'Query model', 'Simulation', 'n-WSS@95%']],
                      how = 'left', on = ['Review', 'Train model', 'Feature model', 'Query model', 'Simulation'])

    df_wss = df_wss.reindex(columns = ['Review', 'Train model', 'Feature model', 'Query model', 'Simulation', 'WSS@95%', 'n-WSS@95%', 'Workload reduction (n)']) ###
    df_wss['Workload reduction (hours)'] = round((df_wss['Workload reduction (n)'] * 0.5 / 60), 1) ###
    
    return df_wss
