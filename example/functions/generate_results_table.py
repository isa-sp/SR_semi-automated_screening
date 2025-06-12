import pandas as pd
import math

def generate_results_table(df_wss, df_prec, data_type = 'original'):

    if data_type == 'original':
        df_wss_prec = pd.merge(df_wss, df_prec, on=['Review', 'Train model', 'Feature model', 'Query model', 'Simulation'])
        column_names = ['Review', 'Train model', 'Feature model']
        index1 = 3
        index2 = 6
    if data_type == 'adapted':
        df_wss_prec = pd.merge(df_wss, df_prec, on=['Review', 'Seed', 'Total records', 'Relevant records', 'Train model', 'Feature model', 'Query model', 'Simulation'])
        column_names = ['Review', 'Seed', 'Total records', 'Relevant records', 'Train model', 'Feature model']
        index1 = 6
        index2 = 9
    df_wss_prec.drop(['Query model'], axis=1, inplace=True)

    # Compute the average WSS at 95% recall including confidence interval
    df_WSS95 = df_wss_prec.groupby(column_names)['WSS@95%'].agg(Mean_WSS95 = 'mean',
                                                                Count_WSS95 = 'count',
                                                                SD_WSS95 = 'std').reset_index()

    ci95_hi_WSS95 = []
    ci95_lo_WSS95 = []

    for i in df_WSS95.index:
        m, c, s = df_WSS95.loc[i][index1:index2]
        ci95_hi_WSS95.append("{:.3f}".format(m + 1.96*s/math.sqrt(c)))
        ci95_lo_WSS95.append("{:.3f}".format(m - 1.96*s/math.sqrt(c)))
    df_WSS95['ci95_hi_WSS95'] = ci95_hi_WSS95
    df_WSS95['ci95_lo_WSS95'] = ci95_lo_WSS95
    df_WSS95['Mean_WSS95'] = df_WSS95['Mean_WSS95'].apply(lambda x: '{:,.3f}'.format(x))

    # Compute the average normalized WSS at 95% recall including confidence interval
    df_nWSS95 = df_wss_prec.groupby(column_names)['n-WSS@95%'].agg(Mean_nWSS95 = 'mean',
                                                                   Count_nWSS95 = 'count',
                                                                   SD_nWSS95 = 'std').reset_index()
    
    ci95_hi_nWSS95 = []
    ci95_lo_nWSS95 = []

    for i in df_nWSS95.index:
        m, c, s = df_nWSS95.loc[i][index1:index2]
        ci95_hi_nWSS95.append("{:.3f}".format(m + 1.96*s/math.sqrt(c)))
        ci95_lo_nWSS95.append("{:.3f}".format(m - 1.96*s/math.sqrt(c)))
    df_nWSS95['ci95_hi_nWSS95'] = ci95_hi_nWSS95
    df_nWSS95['ci95_lo_nWSS95'] = ci95_lo_nWSS95
    df_nWSS95['Mean_nWSS95'] = df_nWSS95['Mean_nWSS95'].apply(lambda x: '{:,.3f}'.format(x))

    # Compute the average precision at 95% recall including confidence interval
    df_prec95 = df_wss_prec.groupby(column_names)['Precision@95%'].agg(Mean_prec95 = 'mean',
                                                                       Count_prec95 = 'count',
                                                                       SD_prec95 = 'std').reset_index()
    ci95_hi_prec95 = []
    ci95_lo_prec95 = []

    for i in df_prec95.index:
        m, c, s = df_prec95.loc[i][index1:index2]
        ci95_hi_prec95.append("{:.3f}".format(m + 1.96*s/math.sqrt(c)))
        ci95_lo_prec95.append("{:.3f}".format(m - 1.96*s/math.sqrt(c)))
    df_prec95['ci95_hi_prec95'] = ci95_hi_prec95
    df_prec95['ci95_lo_prec95'] = ci95_lo_prec95
    df_prec95['Mean_prec95'] = df_prec95['Mean_prec95'].apply(lambda x: '{:,.3f}'.format(x))

    # Compute the average workload reduction in number of records including confidence interval
    df_workred_n = df_wss_prec.groupby(column_names)['Workload reduction (n)'].agg(Mean_workred_n = 'mean',
                                                                                   Count_workred_n = 'count',
                                                                                   SD_workred_n = 'std').reset_index()

    ci95_hi_workred_n = []
    ci95_lo_workred_n = []

    for i in df_workred_n.index:
        m, c, s = df_workred_n.loc[i][index1:index2]
        ci95_hi_workred_n.append("{:.0f}".format(m + 1.96*s/math.sqrt(c)))
        ci95_lo_workred_n.append("{:.0f}".format(m - 1.96*s/math.sqrt(c)))
    df_workred_n['ci95_hi_workred_n'] = ci95_hi_workred_n
    df_workred_n['ci95_lo_workred_n'] = ci95_lo_workred_n
    df_workred_n['Mean_workred_n'] = df_workred_n['Mean_workred_n'].apply(lambda x: '{:,.0f}'.format(x))

    # Compute the average workload reduction in hours including confidence interval
    df_workred_hr = df_wss_prec.groupby(column_names)['Workload reduction (hours)'].agg(Mean_workred_hr = 'mean',
                                                                                        Count_workred_hr = 'count',
                                                                                        SD_workred_hr = 'std').reset_index()

    ci95_hi_workred_hr = []
    ci95_lo_workred_hr = []

    for i in df_workred_hr.index:
        m, c, s = df_workred_hr.loc[i][index1:index2]
        ci95_hi_workred_hr.append("{:.1f}".format(m + 1.96*s/math.sqrt(c)))
        ci95_lo_workred_hr.append("{:.1f}".format(m - 1.96*s/math.sqrt(c)))
    df_workred_hr['ci95_hi_workred_hr'] = ci95_hi_workred_hr
    df_workred_hr['ci95_lo_workred_hr'] = ci95_lo_workred_hr
    df_workred_hr['Mean_workred_hr'] = df_workred_hr['Mean_workred_hr'].apply(lambda x: '{:,.1f}'.format(x))


    # Merge the dataframes into one
    df_wss_prec = pd.merge(df_WSS95[column_names+['Mean_WSS95', 'ci95_hi_WSS95', 'ci95_lo_WSS95']], 
                           df_nWSS95[column_names+['Mean_nWSS95', 'ci95_hi_nWSS95', 'ci95_lo_nWSS95']],
                           how = 'left', on = column_names)
    df_wss_prec = pd.merge(df_wss_prec, 
                           df_prec95[column_names+['Mean_prec95', 'ci95_hi_prec95', 'ci95_lo_prec95']], 
                           how = 'left', on = column_names)
    df_wss_prec = pd.merge(df_wss_prec,
                           df_workred_n[column_names+['Mean_workred_n', 'ci95_hi_workred_n', 'ci95_lo_workred_n']], 
                           how = 'left', on = column_names)
    df_wss_prec = pd.merge(df_wss_prec, 
                           df_workred_hr[column_names+['Mean_workred_hr', 'ci95_hi_workred_hr', 'ci95_lo_workred_hr']], 
                           how = 'left', on = column_names)

    df_wss_prec_all_values = df_wss_prec.copy()
    df_wss_prec_all_values['Models'] = df_wss_prec_all_values['Feature model'] + " - " + df_wss_prec_all_values['Train model']
    
    df_wss_prec['WSS@95%recall (CI)'] = df_wss_prec["Mean_WSS95"] + " (" + df_wss_prec["ci95_lo_WSS95"].astype(str) + "-" + df_wss_prec["ci95_hi_WSS95"].astype(str) + ")"
    df_wss_prec['n-WSS@95%recall (CI)'] = df_wss_prec["Mean_nWSS95"] + " (" + df_wss_prec["ci95_lo_nWSS95"].astype(str) + "-" + df_wss_prec["ci95_hi_nWSS95"].astype(str) + ")"
    df_wss_prec['Precision@95%recall (CI)'] = df_wss_prec["Mean_prec95"] + " (" + df_wss_prec["ci95_lo_prec95"].astype(str) + "-" + df_wss_prec["ci95_hi_prec95"].astype(str) + ")"
    df_wss_prec['Workload reduction in record numbers (CI)'] = df_wss_prec["Mean_workred_n"] + " (" + df_wss_prec["ci95_lo_workred_n"].astype(str) + "-" + df_wss_prec["ci95_hi_workred_n"].astype(str) + ")"
    df_wss_prec['Workload reduction in hours (CI)'] = df_wss_prec["Mean_workred_hr"] + " (" + df_wss_prec["ci95_lo_workred_hr"].astype(str) + "-" + df_wss_prec["ci95_hi_workred_hr"].astype(str) + ")"
    
    df_wss_prec.drop(['Mean_WSS95', 'ci95_hi_WSS95', 'ci95_lo_WSS95', 'Mean_nWSS95', 'ci95_hi_nWSS95', 'ci95_lo_nWSS95', 'Mean_prec95', 'ci95_hi_prec95', 'ci95_lo_prec95',
                      'Mean_workred_n', 'ci95_hi_workred_n', 'ci95_lo_workred_n',  'Mean_workred_hr', 'ci95_hi_workred_hr', 'ci95_lo_workred_hr'], axis=1, inplace=True)

    return df_wss_prec_all_values, df_wss_prec
