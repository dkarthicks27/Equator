"""
In this file we have all the methods : clustering, trial_code, near duplicate identification, conceptual search
So our aim is to have a common tfidf method which can serialise and deserialize it.
Then individual methods for each operation, with their parameters
below is the import section:
"""
import re
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
import pickle
import pandas as pd
import os
from glob import glob
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from datetime import time as timing
from sklearn.random_projection import SparseRandomProjection
from nltk import sent_tokenize
from nltk import word_tokenize


def delete():
    d = int(input("do you want to delete the existing tfidf vector or vectorizer\n1 for deleting vector\n2"
                  " for deleting the vectorizer\n3 for deleting both\n4 for not deleting: "))
    if d == 1:
        os.remove("vectors.pickle")
        print("file removed!!!")
    elif d == 2:
        os.remove("vectorizer.pickle")
        print("file removed!!!")
    elif d == 3:
        os.remove("vectorizer.pickle")
        os.remove("vectors.pickle")
        print("both files removed!!!")
    elif d == 4:
        print("choosing not to delete...\n")

def preprocess(s):
    k = re.sub('[0-9]*', '', s.lower())
    return k

def tfidf(filepath, features=1000, n_gram=(1, 1)):
    """
    so in the above section we just made all our imports now in the below section we are going to write a method
    for finding tfidf vectors this method is called once and it returns a pickle file of the tfidf vector so we
    are going to pickle it, the input parameter for this is
    INPUT PARAMETERS:
        filepath : (list) this is a list of filePaths, for eg: ['/Equator/Onedoc/121.txt','/Equator/Onedoc/134.txt', ... ]
        features : (int) this is the number of features to be included
        n_gram : (tuple) this is the ngram range, it must be a tuple input; default (2, 4)
        stop_words : (string) this is the language, default is 'english'
        decode_error: (string) default is 'ignore', options are 'strict'
        pickleloc: (string) where the pickle file needs to be saved for further use. (mandatory)

    OUTPUT:
        Pickle file: it will be saved to the location provided during input parameter
    """
    print("\nStarting tfidf vectorizer\nTime is: ")
    start = time.time()
    print(start)
    Vectorizer = TfidfVectorizer(input='filename', use_idf=True,
                                 stop_words='english',
                                 decode_error='ignore', max_df=0.50,  sublinear_tf=True, ngram_range=n_gram, preprocessor=preprocess)
    vectors = Vectorizer.fit_transform(filePath)
    # print(len(Vectorizer.get_feature_names()))
    ## please note that you have to pass the vectors generated by tfidf into random projection
    ## please modify it accordingly
    with open('vectorizer.pickle', 'ab') as vec:
        pickle.dump(Vectorizer, vec)
        vec.close()
    with open('vectors.pickle', 'ab') as pcfile:
        pickle.dump(vectors, pcfile)
        pcfile.close()
    X = SparseRandomProjection()
    x = X.fit_transform(vectors)
    # print(x.shape)
    end = time.time()
    print("\ntime take is {} s".format(end-start))
    return x


def clustering(num_cluster, top_n_terms, label):
    """
    so after the tfidf method in the above section now in the below section we are going to write a method
    for near duplicates,
    INPUT PARAMETERS:
        threshold ( default = 0.9 )
    Parameter is threshold, i.e the percentage above which the documents should be matching to be eligible for
    qualifying as near duplicates, if no input is given it will take default as 0.9

    """
    km = KMeans(n_clusters=num_cluster)
    tfidfVectors = pickle.load(open('vectors.pickle', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))
    # vectorizer = tfidfVectorizer
    terms = vectorizer.get_feature_names()
    km.fit_transform(tfidfVectors)
    dic = {'cluster id': km.labels_, 'document id': label}
    clusters = pd.DataFrame(dic)
    # print(clusters)
    clusters.sort_values("cluster id", axis=0, ascending=True, inplace=True)
    tuple_ClusterId2DocId = list(clusters.itertuples(index=False, name=None))
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    top = top_n_terms
    topTermsArray = []
    for i in range(num_cluster):
        top_words = [terms[ind] for ind in order_centroids[i, :top]]
        topTermsArray.append(', '.join(top_words))
    dic1 = {'top n terms': topTermsArray, 'cluster id': [x for x in range(0, num_cluster)]}
    clusterToTopTerms = pd.DataFrame(dic1)
    x = input("do you want to save it(enter 1) or print the output(enter 2): ")
    if x == '1':
        clusterToTopTerms.to_csv('cluster.csv', index=False)
    elif x == '2':
        print(clusterToTopTerms)

    # tuple_clusterId2TopTerms = list(clusterToTopTerms.itertuples(index=False, name=None))

    # print(tuple_clusterId2TopTerms)


def nearDuplicate(arr, minThreshold=0.9, maxThreshold=0.95):
    start = time.time()
    # print("\nstarting time is {}".format(t))
    x = pickle.load(open('vectors.pickle', 'rb'))
    print(x.shape)
    lda = TruncatedSVD(n_components=10000)
    x = lda.fit_transform(x)
    print(x)
    print(x.shape)
    similarity = cosine_similarity(x)
    os.remove("file.csv")
    print("csv removed")
    # print(similarity)
    # print(len(similarity))
    """
    Now let us finish near Duplicates
    now here we are printing all the similar documents respect to each document according to threshold
    """
    array = []
    # obj = {}
    for i in range(0, len(similarity)):
        for j in range(i, len(similarity)):
            if i != j and minThreshold <= similarity[i][j] <= maxThreshold:
                array.append((filePath[i], filePath[j], float(round(similarity[i][j] * 100))))
                if len(array) == 10000:
                    print(len(array))
                    my_df = pd.DataFrame(array, columns=['doc_id', 'duplicate_doc', 'similarity_percent'])
                    with open('file.csv', 'a+') as csv_file:
                        my_df.to_csv(path_or_buf=csv_file, index=False)
                    array.clear()
                    my_df = my_df.iloc[0:0]

    print(len(array))
    if len(array) > 0:
        my_df = pd.DataFrame(array, columns=['doc_id', 'duplicate_doc', 'similarity_percent'])
        with open('file.csv', 'a+') as csv_file:
            my_df.to_csv(path_or_buf=csv_file, index=False)
            array.clear()
            my_df = my_df.iloc[0:0]
    end = time.time()
    print("\ntime take is {} s".format(end - start))
    # for line, val in zip(arr, similarity):
    #     for position, items in zip(labels, val):
    #        # print("\n documents similar to document " + str(line) + " with: ")
            # if (line != position) and (items >= threshold):
            #     array.append("doc " + str(position) + " is " + str(items * 100) + " similar")
            # #    print("doc " + str(position) + " is " + str(items * 100) + " similar to doc " + str(line))
        # if len(array) != 0:
        #     obj[line] = array

    # export = pd.Series(obj)
    # val = input('enter 1 to print the result,  2 to save it as csv: ')
    # if val == '1':
    #     print(pd.Series(obj))
    # elif val == '2':
    #     export.to_csv('Near Duplicates.csv')
    # else:
    #     print('incorrect input')


def classification(trainVec, test, labelTraining):
    """
    Now below let us finish trial_code problem:
    """
    # this is for training
    iteration = 1
    x = pickle.load(open('vectors.pickle', 'rb'))
    train, test = train_test_split(x, train_size=0.05)
    while iteration == 1:
        algorithm = int(input("\n1 for NaiveBayes\n2 for SVM\n3 for Logistic regression: "))
        if algorithm == 1:
            clf = MultinomialNB()
            clf.fit(train, labelTraining)
            predicted = clf.predict(test)
            print("\nThe Output below shows the distribution of label probability corresponding to each documents")
            print("rows- document\ncolumns- label order")
            print(clf.predict_proba(train))
            print("\nThe accuracy of algo is :", end='')
            print(clf.score(train, labelTraining))
            print("Class of Each testing dataset: \n")
            print(predicted)
        elif algorithm == 2:
            svm = SVC(probability=True)
            svm.fit(train, labelTraining)
            predicted = svm.predict(test)
            print("\nThe Output below shows the distribution of label probability corresponding to each documents")
            print("rows- document\ncolumns- label order")
            print(svm.predict_proba(train))
            print("\nThe accuracy of algo is :", end='')
            print(svm.score(train, labelTraining))
            print("Class of Each testing dataset: \n")
            print(predicted)
        elif algorithm == 3:
            logistic = LogisticRegression()
            logistic.fit(train, labelTraining)
            predicted = logistic.predict(test)
            print("\nThe Output below shows the distribution of label probability corresponding to each documents")
            print("rows- document\ncolumns- label order")
            print(logistic.predict_proba(train))
            print("\nThe accuracy of algo is :", end='')
            print(logistic.score(train, labelTraining))
            print("Class of Each testing dataset: \n")
            print(predicted)
        else:
            print("no option like this")
        iteration = int(input("Enter\n1 to continue once more\n2 to End: "))


def conceptualSearch(query, route):
    """
    So now let's go to conceptual search
    """

    # so the LsiAndKNN document is taken as input, it can be a sentence or a string or etc.
    print("\n\n......Conceptual Search.......\n")
    vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))
    if route == '1':
        vectorizer.input = "content"
    # vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))
    vec1 = vectorizer.transform(query)
    #print(vec1)
    #print("\n")
    #print(vectorizer.get_feature_names())
    y = pickle.load(open('vectors.pickle', 'rb'))
    sims = cosine_similarity(vec1, y)
    #print(sims)
    print(filePath)
    answer = input("To save the similarity vector or print the output\nEnter 1 for saving, 2 for printing: ")
    if answer == '1':
        with open('conceptualResult.pickle', 'ab') as concept:
            pickle.dump(sims, concept)
            concept.close()
    elif answer == '2':
        # threshold = int(input("\nenter the threshold to find similarity(range: 0 to 0.99):  "))
        print(len(filePath), len(sims[0]))
        for pos, element in zip(filePath, sims[0]):
            if element >= 0.40:
                print("doc " + str(pos) + " is " + str(element * 100) + "% similar")




if __name__ == '__main__':

    """
    Below is the main function here is where the direction is controlled
    """
    delete()
    filePath = glob('/Users/karthickdurai/Equator/OneDoc/*.txt')
    trainData, testData = train_test_split(filePath, train_size=0.05)
    trainLabels = [1, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5]
    labels = os.listdir(r'/Users/karthickdurai/Equator/OneDoc/')
    runTfidf = input("do you want to run tfidf (y/n): ")
    if runTfidf == 'y':
        tfidfVectorizer = tfidf(filepath=filePath)
    else:
        print("\ngoing to use already pickled tfidf vectorizer...)")
    print("\nnow the vectors are created, Choose the operation which you want to perform")
    operation = input("\n0 for conceptual search\n1 for clustering\n2 for trial_code\n3 for near "
                      "Duplicate identification\nx for openingPickleFiles: ")
    if operation == '1':
        print("\nclustering performing...")
        clustering(num_cluster=10, top_n_terms=3, label=filePath)
    elif operation == '2':
        print("\ntrial_code performing...")
        classification(trainData, testData, trainLabels)
    elif operation == '3':
        print("\nnear Duplicate identification...")
        nearDuplicate(arr=labels)
    elif operation == '0':
        what = input("\nIs the LsiAndKNN a String or a path to document\nEnter 1 for string, 2 for path: ")
        if what == '1':
            query = '''From: Laurel Adams [/o=cw-test/ou=first administrative group/cn=recipients/cn=laurel.adams]
To: Sara Shackleton
Subject: TR Bond Swap Confirmation

Importance:     Normal
Priority:       Normal
Sensitivity:    None

Sara,

Paul wants to know if we have any objections to the attached form of 
confirmation.  Please let me know if you have any concerns.  Thank you!  
---------------------- Forwarded by Laurel Adams/HOU/ECT on 07/31/2000 05:00 
PM ---------------------------'''
            conceptualSearch([query], route=what)
        else:
            conceptualSearch(['/Users/karthickdurai/Equator/OneDoc/126.txt'], route=what)
