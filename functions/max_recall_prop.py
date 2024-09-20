import pandas as pd
import collections

def max_recall_prop(review_dic_ord, proportions):
    review_name = []
    max_recalls = []

    # Maximum recall per review-model and per proportion
    for key, value in review_dic_ord.items():

        review_name.append([key]*len(proportions))
        records = len(review_dic_ord[key])
        inclusions = review_dic_ord[key]['label_included'].sum()

        for i in proportions:

            number_screened = round(float(i*records))

            # Calculate the true positives (TP) as the highest number of positive labels possible before the cutoff
            if inclusions >= number_screened:
                TP = number_screened
            else:
                TP = inclusions

            # Calculate the false negatives (FN) as the smallest number of positive labels after the cutoff
            if inclusions >= number_screened:
                FN = inclusions - number_screened
            else:
                FN = 0

            # Calculate the maximum recall based on the TP and FN
            max_recall = round((TP/(TP+FN)), 2)
            max_recalls.append(max_recall)

    review_name = [item for sublist in review_name for item in sublist]   

    df_max_recalls = pd.DataFrame(list(zip(review_name, max_recalls)))
    df_max_recalls = df_max_recalls.rename(columns={0: 'Review', 1: 'Maximum recall'})
    
    return df_max_recalls
