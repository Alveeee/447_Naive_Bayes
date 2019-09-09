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

#returns the prevalence of each value of each attribute in a class-uniform dataset [F(A_j = a_k, C = c_i)]
def find_attribute_prevalence(class_data, numAttributes):

    #array for storing the total count of each value, for each attribute, in the dataset **Count starts at 1 to conform to mathematical formula**
    table = [[1 for x in range(10)] for x in range(numAttributes)]

    #iterate through each example
    for c in range(len(class_data)):

        #iterate through each attribute
        for a in range(numAttributes):
            #increment count for attribute's matching value
            table[a][int(class_data[c][a])-1] += 1

    #divide the number of examples matching each value by the number of examples in the class
    for attribute in table:
        for i in range(10):
            attribute[i] /= numAttributes + (len(class_data))


    return table

def classify_example(example, learned_set):

    C = []
    for c in range(len(learned_set)):
        C.append(0)
        for a in range(len(example)-1):
            C[c] += learned_set[c][a][int(example[a])-1]
        C[c] *= len(learned_set[c])
        print(len(learned_set[c]))
    high = 0
    prediction = 0
    for c in range(len(learned_set)):
        #print(high)
        if C[c] > high:
            high = C[c]
            prediction = c

    return prediction

def learn_dataset(dataset_name, class_identities, numAttributes):

    learned_set = []
    for identity in class_identities:
        learned_set.append(find_attribute_prevalence(get_class_data(dataset_name, identity), numAttributes))

    return learned_set

    

def print_prevalence(prevalence_table):
    for i in range(len(prevalence_table)):
        total = 0
        for value in prevalence_table[i]:
            print(value)
            total += value
        print(str(total) + '\n')

BCD_identities = ["2","4"]
BCD_examples = ["2,1,1,1,2,1,2,1,1,2".split(","),"10,10,10,4,8,1,8,10,1,4".split(","),"1,1,1,1,2,1,3,2,1,2".split(","),"5,1,3,1,2,1,2,1,1,2".split(",")]
BCD_learned = learn_dataset("BCD-processed.txt",BCD_identities, 9)
for example in BCD_examples:
    print("Predicted class: " + BCD_identities[classify_example(example, BCD_learned)])
