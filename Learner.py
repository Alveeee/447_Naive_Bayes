#returns class-specific dataset(from given dataset) for given class [Q(C = c_i)]
def get_class_data(dataset_name, class_identity):

    #array for storing class-specific dataset
    class_data = []

    #open original dataset
    with open(dataset_name) as dataset:

        #read data
        for line in dataset:
            features = line.split(",")

            #if the class matches the requested identity, add to class-specific dataset
            if features[-1] == class_identity + "\n":
                class_data.append(features)

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
            table[a][int(class_data[c][a])-1] += 1

    #divide the number of examples matching each value by the number of examples in the class
    for attribute in table:
        for i in range(numValues - 1):
            attribute[i] /= numAttributes - 1 + (len(class_data))

    #store sample's class size in probability table
    table[-1][0] = len(class_data)
    
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
            C[c] += learned_set[c][a][int(example[a])-1]

        #multiply sum by sample's class size
        C[c] *= int(learned_set[c][-1][0]) / sample_size
        print("Total for class " + str(c) + ": " + str(C[c]))

    #find highest value in C[] as prediction
    high = 0
    prediction = 0
    for c in range(len(learned_set)):
        if C[c] > high:
            high = C[c]
            prediction = c

    return prediction

#creates array of probability tables for each class in dataset
def learn_dataset(dataset_name, class_identities, numValues):

#3D array - [class][attribute][value]
    learned_set = []

    #find probability table for each class
    for identity in class_identities:
        learned_set.append(find_attribute_probability(get_class_data(dataset_name, identity), numValues))

    return learned_set

#prints out the probability table for given class, useful for debugging
def print_probability(probability_table):
    for i in range(len(probability_table)):
        total = 0
        for value in probability_table[i]:
            print(value)
            total += value
        print(str(total) + '\n')

BCD_identities = ["2","4"]
BCD_examples = ["2,1,1,1,2,1,2,1,1,2".split(","),"10,10,10,4,8,1,8,10,1,4".split(","),"1,1,1,1,2,1,3,2,1,2".split(","),"5,1,3,1,2,1,2,1,1,2".split(",")]
BCD_learned = learn_dataset("BCD-processed.txt",BCD_identities, 10)
for example in BCD_examples:
    print("Predicted class: " + BCD_identities[classify_example(example, BCD_learned)])
