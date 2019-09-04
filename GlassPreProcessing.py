#Glass Pre Processing - Kyle Webster
from random import *

#method processes the Glass Dataset
def processGD(inputName, outputName):
    #open input and output files
    with open(inputName) as readIn:
        with open(outputName, "w") as writeOut:
            #iterate over each line in input file
            for line in readIn:
                #iterate over each feature in line
                features = line.split(",");
                for i in range(1, len(features)):
                    #No need to replace missing data since data fully exists
                    temp = round(float(features[i]), 3)
                    
                    #write data to output file, skipping ID number
                    writeOut.write(str(temp))
                    if i < len(features)-1:
                        writeOut.write(",")

processGD("glass.data","glassProcessed.txt")
                
