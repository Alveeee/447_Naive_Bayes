#Greg Martin
#CSCI447 Votes Preprocessing
#9/4/19

import pandas as pd
import numpy as np

#Preprocessor that determines a percentage of how party members voted on issues.
#Then it randomly picks from weighted options to provide a more appropriate vote.
#i.e. (If 90% of Republicans voted "Yes" on an issue, any missing Republican
#vote has a 90% chance of being a "Yes" and a 10% of being "No"
def weightedPreprocessor(input_file):
    data = pd.read_csv(input_file,header=None,names=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'])
    #Grabs just republican rows
    republican_data = data.loc[(data['0'] == 'republican')]
    #Grabs just democrat rows
    democrat_data = data.loc[(data['0'] == 'democrat')]
    rep_percentages_list = []
    rep_non_weighted_list_of_lists = []

    dem_percentages_list = []
    dem_non_weighted_list_of_lists = []

    #Step through each column of the republican dataframe and
    #calculates the percentages of how members voted on issues.
    for column in republican_data:
        rep_percentages = republican_data[column].value_counts(normalize=True).tolist()
        rep_non_weighted_list = republican_data[column].value_counts().index.tolist()
        rep_percentages_list.append(rep_percentages)
        rep_non_weighted_list_of_lists.append(rep_non_weighted_list)

    for column in democrat_data:
        dem_percentages = democrat_data[column].value_counts(normalize=True).tolist()
        dem_non_weighted_list = democrat_data[column].value_counts().index.tolist()
        dem_percentages_list.append(dem_percentages)
        dem_non_weighted_list_of_lists.append(dem_non_weighted_list)

    options = ['y','n']
    final_data = pd.DataFrame()
    dat_count = 0
    j=0
    #Steps through the original dataframe with the help of some counters and
    #weighted-randomly replaces '?' in the frame based off of the previously
    #observed voting tendencies of each party.
    for column in data:
        counter=0
        #Make a list of each column for easy traversal
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
        #Make a Series object out of the list with potentially newly changed values
        temp_data = pd.Series(data_slice)
        #Build up a new dataframe by appending the Series objects (Keeps positions
        #from original dataframe the same)
        final_data = final_data.append(temp_data,ignore_index=True)
        j+=1
    #Flips rows and columns so that the frame is identical except to the
    #original except with no missing values
    final_data = final_data.transpose()
    #Change to binary for easier algorithm work
    final_data = final_data.replace('y','1')
    final_data = final_data.replace('n','0')
    final_data.to_csv('votes_processed.csv',header=False,index=False)

weightedPreprocessor("house-votes-84.data.csv")
