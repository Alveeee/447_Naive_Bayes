import csv
import random
import pandas
import os

#readCsv reads in the preprocessed data
def readCsv(file):
    data = csv.reader(open(file, "r"))
    data_list = list(data)
    for i in range(len(data_list)):
        for j in range(len(data_list[i])):
            data_list[i] = [float(x) for x in data_list[i]]
    return data_list

#randomize data so that when we select training and test sets, we get a variety of each class
def randomizeData(data):
    randomSet = []
    copy = list(data)
    while len(randomSet) < len(data):
        index = random.randrange(len(copy))
        randomSet.append(copy.pop(index))
    return randomSet

def getClasses(data):
    classes = []
    for i in range(len(data)):
        if(not(data[i][len(data[i])-1] in classes)):
           classes.append(data[i][len(data[i])-1])
    return classes

#kFoldCross is how we split the data into training and test sets using 10 fold cross validation
def kFoldCross(data, splitRatio, k):
    #size of test set (for 100 records and a ratio of .9, it would be 10 records)
    testSize = int(len(data) - len(data) * splitRatio)
    index = k*testSize

    trainSet = list(data)
    testSet = []

    for i in range(testSize):
        testSet.append(trainSet.pop(index))

    return [trainSet, testSet]

#returns class-specific dataset(from given dataset) for given class [Q(C = c_i)]
def get_class_data(data, c):
    #array for storing class-specific dataset
    class_data = []

    #read data
    for line in data:
        #if the class matches the requested identity, add to class-specific dataset
        if line[-1] == c:
            class_data.append(line)
    return class_data

#returns the probability of each value of each attribute in a class-uniform dataset [F(A_j = a_k, C = c_i)]
def find_attribute_probability(class_data, numValues):

    numAttributes = len(class_data[0])


    #array for storing the total count of each value, for each attribute, in the dataset **Count starts at 1 to conform to mathematical formula**
    table = [[1 for x in range(numValues)] for x in range(numAttributes)]

    #iterate through each example
    for c in range(len(class_data)):
        #iterate through each attribute
        for a in range(numAttributes - 1):
            #increment count for attribute's matching value
            #TODO figure out a better way to do this without indexing based on value
            x = int(class_data[c][a])-1
            if(len(table[a]) > x):
                table[a][x] += 1

    #divide the number of examples matching each value by the number of examples in the class
    for attribute in table:
        for i in range(numValues):
            attribute[i] /= numAttributes - 1 + (len(class_data))

    #store sample's class size in probability table
    table[-1][0] = len(class_data)
    #print_probability(table)
    return table

#returns predicted class *index* for example using learned set
def classify_example(example, learned_set):

    #array for storing prediction probabilities
    C = []
    sample_size = 0
    #iterate over each class' probability table
    for c in range(len(learned_set)):
        C.append(0)
        sample_size += len(learned_set[c])

        #iterate over each attribute in example
        for a in range(len(example)-1):

            #add the probability from example's attribute value
            x = int(example[a])-1
            if(len(learned_set[c][a]) > x):
                C[c] += learned_set[c][a][x]

    #find highest value in C[] as prediction
    high = 0
    prediction = 0
    for c in range(len(learned_set)):
        if C[c] > high:
            high = C[c]
            prediction = c

    return prediction

#creates array of probability tables for each class in dataset
def learn_dataset(data, classes, n):

    #3D array - [class][attribute][value]
    learned_set = []

    #find probability table for each class
    for c in classes:
        learned_set.append(find_attribute_probability(get_class_data(data, c), n))

    return learned_set

#prints out the probability table for given class, useful for debugging
def print_probability(probability_table):
    for i in range(len(probability_table)):
        total = 0
        for value in probability_table[i]:
            print(value)
            total += value
        print(str(total) + '\n')

#First of the loss functions. MSE is a great way to measure quality,
#however it is harsh on data points that are farther away from zero because
#of the square.
def find_MSE(pred,act):
    total = 0
    size = len(act)
    for i in range(0,size):
        dif_squared = (pred[i] - act[i])**2
        total += dif_squared
    MSE = total/size
    print("Mean Square Error = :",MSE)

def findError(true, false):
    error = (false)/(true+false)
    print("Error is: ",error)


#Second loss function MAE is the same as MSE except it has absolute values
#and no squaring of the diffence between the estimated values and the actual
#values
def find_MAE(pred,act):
    total = 0
    size = len(act)
    for i in range(0,size):
        abs_dif = abs(pred[i] - act[i])
        total += abs_dif
    MAE = total/size
    print("Mean Absolute Error = :",MAE)


#TODO: STILL AN OUT OF BOUND ERROR
def jumble(file):
    data =  pandas.read_csv(file,header=None)
    size = len(data.columns)
    #Uniquely sample numbers in the range of the number of columns in our
    #dataframe. Only selects 10% of numbers
    random_list = random.sample(list(range(size)),int(size/10))

    randomized_features = data
    #Gets the columns at the randomly selected spots
    random_set = randomized_features.loc[:,random_list]
    #Creates a new dataframe with these columns dropped
    with_drop = randomized_features.drop(random_set,axis=1)
    #Shuffles the entire column
    random_set = random_set.sample(frac=1)
    #Resets index so that the change actually takes place
    random_set.reset_index(inplace=True, drop=True)
    #Inserts shuffled column(s) back into place
    for l in random_list:
        with_drop.insert(l,l,random_set[l])
    temp = os.path.splitext(file)[0]
    with_drop.to_csv(temp+'_jumbled.csv',header=False,index=False)

def driver(file):
    #reading in data from file
    data = readCsv(file)
    jumble(file)
    data = randomizeData(data)

    splitRatio = .9
    kfold = 10
    result = []
    y = []
    y_bar = []
    y_FP_FN = 0
    y_TP_TN = 0
    for i in range(kfold):
        classes = getClasses(data)

        trainingSet, testSet = kFoldCross(data, splitRatio, i)

        learned = learn_dataset(trainingSet,classes,25))

        correct = 0
        for example in testSet:
            prediction = classes[classify_example(example, learned)]
            y.append(prediction)
            y_bar.append(example[len(example)-1])
            if(example[len(example)-1] == prediction):
                correct += 1
                y_TP_TN += 1
            else:
                y_FP_FN += 1

        result.append(correct/len(testSet))

    #Find Mean Square Error
    find_MSE(y,y_bar)
    #Find Mean Absolute Error
    find_MAE(y,y_bar)
    #Find confusion table based error
    findError(y_TP_TN,y_FP_FN)

    #sum all 10 results to get an average acuracy
    add = 0
    for x in range(len(result)):
        add = add + result[x]
    average = (add/len(result))*100

    print("This algorithm was %{0:.2f} accurate on {1}".format(average,file))

driver("data/BCD-processed.csv")
driver("data/BCD-processed_jumbled.csv")
driver("data/votes_processed.csv")
driver("data/votes_processed_jumbled.csv")
driver("data/soybean-processed.csv")
driver("data/soybean-processed_jumbled.csv")
driver("data/iris-processed.csv")
driver("data/iris-processed_jumbled.csv")
driver("data/glass-processed.csv")
driver("data/glass-processed_jumbled.csv")


##BCD_identities = [2,4]
##BCD_examples = ["2,1,1,1,2,1,2,1,1,2".split(","),"10,10,10,4,8,1,8,10,1,4".split(","),"1,1,1,1,2,1,3,2,1,2".split(","),"5,1,3,1,2,1,2,1,1,2".split(",")]
##BCD_learned = learn_dataset("BCD-processed.txt",BCD_identities, 10)
##
##Vote_identities = [0,1]
##Vote_examples = ["0,1,0,1,1,1,0,0,0,1,0,1,1,1,0,1".split(","),"0,1,0,1,1,1,0,0,0,1,0,1,1,1,0,1".split(","),"1,0,1,0,0,0,1,1,1,1,0,0,0,0,1,0".split(","),"1,1,1,0,0,0,1,1,1,0,0,0,0,0,1,0".split(",")]
##Vote_learned = learn_dataset("house-votes_processed.csv",Vote_identities, 2)
##
##Soybean_identities = [1,2,3,4]
##Soybean_examples =["4,0,2,1,1,1,0,1,0,2,1,1,0,2,2,0,0,0,1,0,3,1,1,1,0,0,0,0,4,0,0,0,0,0,0,1".split(","),"5,0,0,2,0,3,2,1,0,2,1,1,0,2,2,0,0,0,1,0,0,3,0,0,0,2,1,0,4,0,0,0,0,0,0,2".split(","),"0,1,2,0,0,1,1,1,1,1,1,0,0,2,2,0,0,0,1,0,1,1,0,1,1,0,0,3,4,0,0,0,0,0,0,3".split(","),"2,1,2,1,1,3,1,2,1,2,1,1,0,2,2,0,0,0,1,0,2,2,0,1,0,0,0,3,4,0,0,0,0,0,1,4".split(",")]
##Soybean_learned = learn_dataset("soybean-preprocessed.csv",Soybean_identities, 6)
##
##for example in Soybean_examples:
##    print("Soybean Predicted class: " + str(classify_example(example, Soybean_learned)))
##
##for example in Vote_examples:
##    print("Vote Predicted class: " + str(classify_example(example, Vote_learned)))
##
##for example in BCD_examples:
##    print("BCD Predicted class: " + str(BCD_identities[classify_example(example, BCD_learned)]))
