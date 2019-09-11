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
    
    #Get the first column (republicans and democrats)
    temp = data['0']
    #Remove the first column
    data.drop('0',axis=1, inplace=True)
    #insert temp at the right
    data = pd.concat([data,temp],axis=1)
    
    #Change to binary for easier algorithm work
    data = data.replace('y','1')
    data = data.replace('n','0')
    data = data.replace('republican','1')
    data = data.replace('democrat','0')
    data = data.replace('?','2')
    data.to_csv('../data/votes_processed.csv',header=False,index=False)

weightedPreprocessor("../data/house-votes-84.data.csv")
