#Greg Martin
#CSCI447 Votes Preprocessing
#9/4/19

import pandas as pd
import numpy as np
import random as rand

#Preprocessor that determines a percentage of how party members voted on issues.
#Then it randomly picks from weighted options to provide a more appropriate vote.
#i.e. (If 90% of Republicans voted "Yes" on an issue, any missing Republican
#vote has a 90% chance of being a "Yes" and a 10% of being "No"
def weightedPreprocessor(input_file):
    data = pd.read_csv(input_file,header=None,names=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'])
    republican_data = data.loc[(data['0'] == 'republican')]
    democrat_data = data.loc[(data['0'] == 'democrat')]
    republican_vote_filler = []
    rep_percentages_list = []
    rep_non_weighted_list_of_lists = []

    democrat_vote_filler = []
    dem_percentages_list = []
    dem_non_weighted_list_of_lists = []

    for column in republican_data:
        rep_percentages = republican_data[column].value_counts(normalize=True).tolist()
        rep_non_weighted_list = republican_data[column].value_counts().index.tolist()
        rep_random_vote = np.random.choice(rep_non_weighted_list,p=rep_percentages)
        while(rep_random_vote == '?'):
            rep_random_vote = np.random.choice(rep_non_weighted_list,p=rep_percentages)
        republican_vote_filler.append(rep_random_vote)
        rep_percentages_list.append(rep_percentages)
        rep_non_weighted_list_of_lists.append(rep_non_weighted_list)

    for column in democrat_data:
        dem_percentages = democrat_data[column].value_counts(normalize=True).tolist()
        dem_non_weighted_list = democrat_data[column].value_counts().index.tolist()
        dem_random_vote = np.random.choice(dem_non_weighted_list,p=dem_percentages)
        while(dem_random_vote == '?'):
            dem_random_vote = np.random.choice(dem_non_weighted_list,p=dem_percentages)
        democrat_vote_filler.append(dem_random_vote)
        dem_percentages_list.append(dem_percentages)
        dem_non_weighted_list_of_lists.append(dem_non_weighted_list)

    options = ['y','n']
    final_data = pd.DataFrame()
    dat_count = 0
    j=0
    for column in data:
        counter=0
        data_slice = data[column].to_list()
        for i in range(len(data_slice)):
            if(data_slice[i] == '?'):
                if(counter in republican_data.index.tolist()):
                    tempVar = np.random.choice(rep_non_weighted_list_of_lists[j],p=rep_percentages_list[j])
                    while(tempVar == '?'):
                        tempVar = np.random.choice(rep_non_weighted_list_of_lists[j],p=rep_percentages_list[j])         
                    data_slice[i] = tempVar
                    dat_count+=1
                else:
                    tempVar = np.random.choice(dem_non_weighted_list_of_lists[j],p=dem_percentages_list[j])
                    while(tempVar == '?'):
                        tempVar = np.random.choice(dem_non_weighted_list_of_lists[j],p=dem_percentages_list[j])           
                    data_slice[i] = tempVar
                    dat_count+=1
                counter+=1
        temp_data = pd.Series(data_slice)
        final_data = final_data.append(temp_data,ignore_index=True)
        j+=1
    final_data = final_data.transpose()
    final_data.to_csv('votes_processed.csv',header=False,index=False)

weightedPreprocessor("house-votes-84.data.csv")
