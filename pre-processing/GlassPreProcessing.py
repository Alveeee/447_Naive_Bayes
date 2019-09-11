#Glass Pre Processing - Kyle Webster
import csv

#Reading and descretizing data from a CSV
def readCsv(file):
    lines = csv.reader(open(file,"r"))
    data = list(lines)
    high = [-1 for x in range(10)]
    low = [20000 for x in range(10)]
    #for loop for each row of data
    for i in range(len(data)):

        #for loop for each element within a row
        for j in range(len(data[i])):

            #This both rounds each point to the nearest 3rd decemal place, then drops the decimal point for easier categorization
            data[i][j] = int(1000*round(float(data[i][j]),3))

            ##Serves to further descretize data into integers between 0 and #number
            #23
            if (j == 0):
                data[i][j] = 1534 - data[i][j]
            #14
            else if (j == 1):
                data[i][j] = round(data[i][j]/500) - 21
            #22
            else if (j == 2):
                data[i][j] = round(data[i][j]/200)
            #17
            else if (j == 3):
                data[i][j] = round(data[i][j]/200) - 1
            #19
            else if (j == 4):
                data[i][j] = round((data[i][j]-70000)/300)+1
            #25
            else if (j == 5):
                data[i][j] = round(data[i][j]/100)
                if data[i][j] > 25:
                    data[i][j] = 25
            #21
            else if (j == 6):
                data[i][j] = round((data[i][j]-5500)/500)
            #16
            else if (j == 7):
                data[i][j] = round(data[i][j]/200)
            #5
            else if (j == 8):
                data[i][j] = round(data[i][j]/100)
            #6
            else if (j == 9):
                data[i][j] = round(data[i][j]/1000)-1

            if (data[i][j] > high[j]):
                high[j] = data[i][j]
            if (data[i][j] < low[j]):
                low[j] = data[i][j]

    for n in range(len(high)):
        print("Feature: " + str(n))
        print("High: " + str(high[n]))
        print("Low: " + str(low[n]))

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
    oFile = "../data/glass-processed.csv"
    #collect data from CSV
    data = readCsv(iFile)
    #Writes data to CSV
    writeCsv(oFile, data)

main()
