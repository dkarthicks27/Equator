"""
In this file we have all the methods : clustering, trial_code, near duplicate identification, conceptual search
So our aim is to have a common tfidf method which can serialise and deserialize it.
Then individual methods for each operation, with their parameters
below is the import section:
"""
from pprint import pprint
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
import pickle
import pandas as pd
import sys
import re
import os
from glob import glob
from sklearn.cluster import KMeans
from sklearn.svm import SVC
import pyodbc


def sql_connect(server="KARTHICK\SQLEXPRESS", database="EQUATOR"):
    try:
        conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=KARTHICK\SQLEXPRESS;"
            "Database=EQUATOR;"
            "Trusted_Connection=yes;"
        )
    except:
        print("Oops!", sys.exc_info()[0], "occured.\n")
        return "unable to connect"
    else:
        return conn


def close_sql_connection(connection):
    try:
        connection.close()
    except:
        print("Oops!", sys.exc_info()[0], "occured.\n")
        return 0
    else:
        return 1


def read_sql_input(connection, read_statement):
    try:
        cursor = connection.cursor()
        cursor.execute(read_statement)
        # fetchall is risky as all the rows are loaded on to memory, so it is better to fetch one row at a time
        # rows = cursor.fetchall() must be avoided in most cases
        # instead we can use a while loop like this and give the exit condition as row being empty
        array = []
        for row in cursor:
            array.append(row)
        return array
    except:
        print("Oops!", sys.exc_info()[0], "occured.\n")
    finally:
        connection.close()


def insert_sql(connection, insert_statement, values):
    try:
        cursor = connection.cursor()
        cursor.executemany(insert_statement, values)
        cursor.commit()
    except:
        print("Oops!", sys.exc_info(), "occured.\n")
    finally:
        connection.close()


def insert_near_dups():
    conn = sql_connect()
    sql = "INSERT INTO near_dup_input_view VALUES (?, ?)"
    values = []
    for x, y in zip(range(1, len(filePath)), filePath):
        values.append((x, y))
    pprint(values)
    insert_sql(conn, sql, values)


def truncate_sql_table(connection, sql_statement):
    try:
        cursor = connection.cursor()
        cursor.execute(sql_statement)
        cursor.commit()
    except:
        print("Oops!", sys.exc_info()[0], "occured.\n")
    finally:
        connection.close()




#####################################################################################################################


def delete(d):
    # d = int(input("do you want to delete the existing tfidf vector or vectorizer\n1 for deleting vector\n2"
    # " for deleting the vectorizer\n3 for deleting both\n4 for not deleting: "))
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


##################################################################################################################


def preprocess(s):
    k = re.sub('[0-9]', '', s)
    return s


def tfidf(filepath, features=1000, n_gram=(2, 4)):
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
    question = input("\nDo you want to replace the existing tfidf vectors, vectorizer or both\n"
                     "1 for tfidf_vectors\n2 for tfidf_vectorizer\n3 for both\n4 for none: ")
    if question == '1':
        delete(1)
    if question == '2':
        delete(2)
    if question == '3':
        delete(3)
    if question == '4':
        delete(4)
    Vectorizer = TfidfVectorizer(input='filename', max_features=features, ngram_range=n_gram,
                                 stop_words='english',
                                 decode_error='ignore', preprocessor=preprocess)
    vectors = Vectorizer.fit_transform(filePath)
    # vectors = tfidfVectorizer.transform(filepath)
    with open('vectorizer.pickle', 'ab') as vec:
        pickle.dump(Vectorizer, vec)
        vec.close()
    with open('vectors.pickle', 'ab') as pcfile:
        pickle.dump(vectors, pcfile)
        pcfile.close()
    return Vectorizer


####################################################################################################################


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
    # print(dic1)
    clusterToTopTerms = pd.DataFrame(dic1)
    x = input("do you want to save it(enter 1) or print the output(enter 2): ")
    if x == '1':
        clusterToTopTerms.to_csv('cluster.csv', index=False)
        tuple_values = list(clusterToTopTerms.itertuples(index=False, name=None))
        try:
            connect = sql_connect()
            truncate_sql_table(connect, "TRUNCATE TABLE clustering")
            connect = sql_connect()
            sql = "INSERT INTO clustering VALUES (?, ?)"
            insert_sql(connect, sql, tuple_values)
        except:
            print("Oops!", sys.exc_info()[0], "occured.\n")
    elif x == '2':
        print(clusterToTopTerms)

    # tuple_clusterId2TopTerms = list(clusterToTopTerms.itertuples(index=False, name=None))

    # print(tuple_clusterId2TopTerms)


####################################################################################################################


def nearDuplicate(arr, threshold=0.9):
    x = pickle.load(open('vectors.pickle', 'rb'))
    similarity = cosine_similarity(x)
    """
    Now let us finish near Duplicates
    now here we are printing all the similar documents respect to each document according to threshold
    """
    array = []
    for line, val in zip(arr, similarity):
        for position, items in zip(labels, val):
            # print("\n documents similar to document " + str(line) + " with: ")
            if (line != position) and (items >= threshold):
                array.append((line, position, round(items * 100)))
                # string = string + " doc " + str(position) + " is " + str(items * 100) + " similar"
                # print("doc " + str(position) + " is " + str(items * 100) + " similar to doc " + str(line))
        # if len(string) != 0:
        # obj[line] = string
    imports = pd.DataFrame(array, columns=['doc_id', 'duplicate_doc', 'similarity_percent'])
    pprint(imports)
    val = input('enter 1 to print the result,  2 to save it as csv: ')
    if val == '1':
        print(imports)
    elif val == '2':
        imports.to_csv('Near Duplicates.csv')
        # tuple_nearDups = list(imports.itertuples(index=False, name=None))
        # print(tuple_nearDups)
        try:
            connect = sql_connect()
            truncate_sql_table(connect, "TRUNCATE TABLE near_duplicates")
            connect = sql_connect()
            sql = "INSERT INTO near_duplicates VALUES (?, ?, ?)"
            insert_sql(connect, sql, array)
        except Exception as e:
            print("Oops!", e, "occured.\n")

    else:
        print('incorrect input')


#################################################################################################################


def classification(trainVec, test, labelTraining):
    """
    Now below let us finish trial_code problem:
    """
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


###################################################################################################################
def hierarchial_clustering():
    from sklearn.cluster import AgglomerativeClustering

    vectors = pickle.load(open('vectors.pickle', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))
    cluster = AgglomerativeClustering(n_clusters=10, affinity="euclidean", linkage="ward")
    x = cluster.fit_predict(vectors.toarray())
    # dic = {'cluster id': cluster.labels_, 'document id': range(0, 479)}
    # clusters = pd.DataFrame(dic)
    # print(clusters)
    df = pd.DataFrame(vectors.toarray(), columns=vectorizer.get_feature_names())
    # print(df)
    df['cluster'] = cluster.labels_
    # print(df)
    dataFrame = df.groupby('cluster').sum()
    # print(dataFrame)
    # k = dict(dataFrame.sort_values(by=0, axis=1, ascending=False).iloc[0, 0: 4])
    # dic1 = {'top n terms': [i for i in k.keys()], 'cluster id': 0}
    # print(dic1)
    # top_n_words = int(input("enter the top x words you want to filter: "))
    top_n_words = 4
    connection = sql_connect()
    cursor = connection.cursor()
    sql = "INSERT INTO hierarchial_clustering VALUES (?, ?)"
    truncate_sql_table(connection, "TRUNCATE TABLE hierarchial_clustering")
    for i in range(0, 10):
        # print(i)
        connection = sql_connect()
        # print(dataFrame.sort_values(by=i, axis=1, ascending=False).iloc[i, 0: top_n_words])
        k = dict(dataFrame.sort_values(by=i, axis=1, ascending=False).iloc[i, 0: top_n_words])
        dic1 = {'top n terms': [', '.join([str(elem) for elem in k.keys()])], 'cluster id': i}
        output = pd.DataFrame(dic1)
        tuple_values = output.itertuples(index=False, name=None)
        insert_sql(connection, sql, list(tuple_values))
        # cursor.executemany(sql, list(tuple_values))
        # cursor.commit()
        # print(dic1)


#######################################################################################################################


def conceptualSearch(query, route):
    """
    So now let's go to conceptual search
    """

    # so the query document is taken as input, it can be a sentence or a string or etc.
    print("\n\n......Conceptual Search.......\n")
    if route == '1':
        tfidfVectorizer.input = "content"
    vec1 = pickle.load(open('vectorizer.pickle', 'rb'))
    vec1 = vec1.transform(query)
    # vec1 = tfidfVectorizer.transform(query)
    y = pickle.load(open('vectors.pickle', 'rb'))
    sims = cosine_similarity(vec1, y)
    answer = input("To save the similarity vector or print the output\nEnter 1 for saving, 2 for printing: ")
    if answer == '1':
        with open('conceptualResult.pickle', 'ab') as concept:
            pickle.dump(sims, concept)
            concept.close()
    elif answer == '2':
        # threshold = int(input("\nenter the threshold to find similarity(range: 0 to 0.99):  "))
        for pos, element in zip(labels, sims[0]):
            if element >= 0.017:
                print("doc " + str(pos) + " is " + str(element * 100) + "% similar")


######################################################################################################################


if __name__ == '__main__':

    """
    Below is the main function here is where the direction is controlled
    """
    filePath = glob(r'C:/Users/Karthick/Documents/EquatorTech/Equator/OneDoc/*.txt')
    trainData, testData = train_test_split(filePath, train_size=0.05)
    trainLabels = [1, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5]
    labels = os.listdir(r'C:/Users/Karthick/Documents/EquatorTech/Equator/OneDoc/')
    runTfidf = input("\ndo you want to run tfidf (y/n): ")
    if runTfidf == 'y':
        tfidfVectorizer = tfidf(filepath=filePath)
    else:
        print("\ngoing to use already pickled tfidf vectorizer...)")
    print("\nnow the vectors are created, Choose the operation which you want to perform")
    operation = input("\n0 for conceptual search\n1 for clustering\n2 for trial_code\n3 for near "
                      "Duplicate identification\n4 for heirarchial clustering: ")
    if operation == '1':
        print("\nclustering performing...")
        clustering(num_cluster=5, top_n_terms=3, label=filePath)

    elif operation == '2':
        print("\ntrial_code performing...")
        classification(trainData, testData, trainLabels)

    elif operation == '3':
        print("\nnear Duplicate identification...")
        nearDuplicate(arr=labels)

    elif operation == '0':
        what = input("\nIs the query a String or a path to document\nEnter 1 for string, 2 for path: ")
        if what == '1':
            query = input("enter the search query: ")
            conceptualSearch([query], route=what)
        else:
            conceptualSearch([r'C:/Users/Karthick/Documents/EquatorTech/Equator/OneDoc/40.txt'], route=what)

    elif operation == '4':
        hierarchial_clustering()
