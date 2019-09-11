#Breast Cancer Dataset Pre Processing - Alexander Alvarez

from random import *

#method processes the Breast Cancer Dataset
def processBCD(input_name, output_name):

    #open input and output files
    with open(input_name) as readIn:
        with open(output_name, "w") as writeOut:

            #iterate over each line in input file
            for line in readIn:

                #iterate over each feature in line
                features = line.split(",");
                for i in range(1, len(features)):

                    #replace missing datapoints with random int
                    if "?" in features[i]:
                        features[i] = str(randint(1, 10))

                    #write data to output file, skipping ID number
                    writeOut.write(features[i])
                    if i < len(features)-1:
                        writeOut.write(",")
                

processBCD("../data/breast-cancer-wisconsin.data","../data/BCD-processed.csv")
