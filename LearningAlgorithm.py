#returns class-specific dataset(from given dataset) for given class
def get_class_data(dataset_name, class_identity):

    #array for storing class-specific dataset
    class_data = []

    #open original dataset
    with open(dataset_name) as dataset:

        #read data
        for line in dataset:
            datastream = line.split(",")

            #if the class matches the requested identity, add to class-specific dataset
            if features[-1] == class_identity:
                class_data.append(features)

    return class_data

#returns the prevalence of each value of each attribute in a class-uniform dataset
def find_attribute_prevalence(class_data, numAttributes):

    #array for storing the total count of each value, for each attribute, in the dataset **Count starts at 1 to conform to mathematical formula**
    totals = [[1 for x in range(10)] for x in range(numAttributes)]

    #iterate through each example
    for c in range(len(class_data)):

        #iterate through each attribute
        for a in range(numAttributes):

            #increment count for attribute's matching value
            totals[a][class_data[c][a]] += 1

    #divide the number of examples matching each value by the number of examples in the class
    for attribute in totals:
        for i in range(10):
            attribute[i] /= numAttributes + (len(class_data))


    return totals

