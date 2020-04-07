"""
In this file we have all the methods : clustering, classification, near duplicate identification, conceptual search
So our aim is to have a common tfidf method which can serialise and deserialize it.
Then individual methods for each operation, with their parameters
below is the import section:
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import pandas as pd
import os
from glob import glob
from sklearn.cluster import KMeans

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


def tfidf(filepath, features=1000, n_gram=(2, 4)):
    tfidfVectorizer = TfidfVectorizer(input='filename', max_features=features, ngram_range=n_gram, stop_words='english',
                                      decode_error='ignore')
    vectors = tfidfVectorizer.fit_transform(filepath)
    # with open('vectorizer.pickle', 'ab') as vec:
    # pickle.dump(tfidfVectorizer, vec)
    # vec.close()
    with open('vectors.pickle', 'ab') as pcfile:
        pickle.dump(vectors, pcfile)
        pcfile.close()
    return tfidfVectorizer


"""
so after the tfidf method in the above section now in the below section we are going to write a method
for near duplicates,
INPUT PARAMETERS:
    threshold ( default = 0.9 )
Parameter is threshold, i.e the percentage above which the documents should be matching to be eligible for 
qualifying as near duplicates, if no input is given it will take default as 0.9

"""


def clustering(num_cluster, top_n_terms, label):
    km = KMeans(n_clusters=num_cluster)
    tfidfVectors = pickle.load(open('vectors.pickle', 'rb'))
    vectorizer = tfidfVectorizer
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
    clusterToTopTerms.to_csv('cluster.csv', index=False)
    # tuple_clusterId2TopTerms = list(clusterToTopTerms.itertuples(index=False, name=None))

    # print(tuple_clusterId2TopTerms)


"""
Now let us finish near Duplicates
"""


def nearDuplicate(arr, threshold=0.9):
    x = pickle.load(open('vectors.pickle', 'rb'))
    similarity = cosine_similarity(x)
    """
    now here we are printing all the similar documents respect to each document according to threshold
    """
    obj = {}
    for line, val in zip(arr, similarity):
        array = []
        for position, items in zip(labels, val):
            # print("\n documents similar to document " + str(line) + " with: ")
            if (line != position) and (items >= threshold):
                array.append("doc " + str(position) + " is " + str(items * 100) + " similar")
                # print("doc " + str(position) + " is " + str(items * 100) + " similar to doc " + str(line))
        if len(array) != 0:
            obj[line] = array

    export = pd.Series(obj)
    val = input('enter 1 to print the result,  2 to save it as csv: ')
    if val == '1':
        print(pd.Series(obj))
    elif val == '2':
        export.to_csv('Near Duplicates.csv')
    else:
        print('incorrect input')


"""
Now below let us finish classification problem:
"""


def classification():
    pass


"""
Below is the main function here is where the direction is controlled
"""
if __name__ == '__main__':
    filePath = glob('/Users/karthickdurai/Equator/OneDoc/*.txt')
    labels = os.listdir(r'/Users/karthickdurai/Equator/OneDoc/')
    runTfidf = input("do you want to run tfidf (y/n): ")
    if runTfidf == 'y':
        tfidfVectorizer = tfidf(filepath=filePath)
    else:
        print("going to use already pickled tfidf vectorizer...)")
    print("now the vectors are created, Choose the operation which you want to perform")
    operation = input("Enter 1 for clustering, 2 for classification, 3 for near Duplicate identification: ")
    if operation == '1':
        print("clustering performing...")
        clustering(num_cluster=5, top_n_terms=3, label=labels)
    elif operation == '2':
        print("classification performing...")
    elif operation == '3':
        print("near Duplicate identification...")
        nearDuplicate(arr=labels)
    else:
        print("incorrect response")
