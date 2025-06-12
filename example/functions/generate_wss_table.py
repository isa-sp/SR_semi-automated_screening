import pandas as pd

def generate_wss_table(evaluation, n_simulations, data_type = 'original'):

    df_wss = pd.DataFrame()
    length = n_simulations
    
    for key, value in evaluation.items():
        
        names = key.split('_')
        review = [names[0]] * length
        
        if data_type == 'original':
            train_model = [names[1]] * length
            feature_model = [names[2]] * length
            query_model = [names[3]] * length
            
        if data_type == 'adapted':
            total_records = [names[1]] * length
            rel_records = [names[2]] * length
            train_model = [names[3]] * length
            feature_model = [names[4]] * length
            query_model = [names[5]] * length
            seed = [names[6]] * length
            
        simulations = range(1, n_simulations+1)
        wss = value[0][2]['WSS-95%']
        nwss = value[0][5]['nWSS-95%']
        n_saved = value[0][3]['Workload reduction (records)']
        
        if data_type == 'original':
            df_sim = pd.DataFrame(list(zip(review, train_model, feature_model, query_model, simulations, wss, nwss, n_saved)),
                                   columns = ['Review', 'Train model', 'Feature model', 'Query model', 'Simulation', 'WSS@95%', 'n-WSS@95%', 'Workload reduction (n)'])
        if data_type == 'adapted':
            df_sim = pd.DataFrame(list(zip(review, seed, total_records, rel_records, train_model, feature_model, query_model, simulations, wss, nwss, n_saved)),
                                    columns = ['Review', 'Seed', 'Total records', 'Relevant records', 'Train model', 'Feature model', 'Query model', 'Simulation', 'WSS@95%', 'n-WSS@95%', 'Workload reduction (n)'])
        df_wss = pd.concat([df_wss, df_sim])

        df_wss = df_wss.reset_index(drop = True)

    df_wss['Workload reduction (hours)'] = round((df_wss['Workload reduction (n)'] * 0.5 / 60), 1) ###
    
    return df_wss
