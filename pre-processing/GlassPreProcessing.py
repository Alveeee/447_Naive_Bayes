#Glass Pre Processing - Kyle Webster
import csv

#Reading and descretizing data from a CSV
def readCsv(file):
    lines = csv.reader(open(file,"r"))
    data = list(lines)
    #for loop for each row of data
    for i in range(len(data)):
        #for loop for each element within a row
        for j in range(len(data[i])):
            data[i][j] = round(float(data[i][j]), 3)
    return data

#function to write data to a CSV File
def writeCsv(file, data):
    with open(file, mode='w') as out:
        #writes each row from the data
        writer = csv.writer(out, delimiter=',')
        for i in data:
            writer.writerow(i)

def main():
    #Read CSV file
    iFile = "../data/glass.data.csv"
    oFile = "../data/glass-preprocessed.csv"
    #collect data from CSV
    data = readCsv(iFile)
    #Writes data to CSV
    writeCsv(oFile, data)

main()
