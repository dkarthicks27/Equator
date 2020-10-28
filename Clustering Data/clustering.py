import os
import pandas as pd
import nltk
import re
import glob

path = "/home/eqt2/50K Text Docs/"
file_paths = (glob.glob(path + "*.txt"))
files = os.listdir(path)
file_names = []
file_list = []

for file in files:
    file_names.append(file)


#############################################################################################################
def tokenize_and_stem(text):
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z0-9]', token):
            filtered_tokens.append(token)
    # stems = [stemmer.stem(t) for t in filtered_tokens]
    return filtered_tokens


##################################################################################################################
# total_vocab = []
# for i in file_list:
#    total_vocab.extend(tokenize_and_stem(i))


#################################################################################################################
from sklearn.feature_extraction.text import TfidfVectorizer

tfid_vectorizer = TfidfVectorizer(max_df=0.75, min_df=0.25, stop_words="english", use_idf=True,
                                  ngram_range=(1, 1), input='filename', decode_error='ignore')
tfidf_matrix = tfid_vectorizer.fit_transform(file_paths)

terms = tfid_vectorizer.get_feature_names()

##################################################################################################################
from sklearn.cluster import KMeans

num_clusters = 20
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)

# the below block maps cluster id to document id
# s1 = pd.Series(km.labels_, name='cluster id')
# s2 = pd.Series(file_names, name='document id')
# dic = pd.concat([s1, s2], axis=1)

##################################################################################################################
dic = {'cluster id': km.labels_, 'document id': file_names}
clusters = pd.DataFrame(dic)
# print(clusters)
clusters.sort_values("cluster id", axis=0, ascending=True, inplace=True)
tuple_ClusterId2DocId = list(clusters.itertuples(index=False, name=None))
# print(tuple_ClusterId2DocId)
# print('\n')


#################################################################################################################
# this below block represents the cluster_id to top 10 terms in that cluster
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
top = 5
topTermsArray = []
for i in range(num_clusters):
    top_words = [terms[ind] for ind in order_centroids[i, :top]]
    topTermsArray.append(', '.join(top_words))

#################################################################################################################
dic1 = {'top n terms': topTermsArray, 'cluster id': [x for x in range(0, num_clusters)]}
clusterToTopTerms = pd.DataFrame(dic1)
tuple_clusterId2TopTerms = list(clusterToTopTerms.itertuples(index=False, name=None))
# print(tuple_clusterId2TopTerms)

##############################################################################################################
# below is the syntax for trial_code
# Y = tfid_vectorizer.transform(["why do i need to send a mail"])
# prediction = km.predict(Y)
# print(prediction)
##################################################################################################################

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="demo",
    passwd="demo123",
    database="mydb"
)
myCursor = mydb.cursor()
# myCursor.execute("SHOW TABLES")

sql = "DELETE FROM clusterToDoc"
myCursor.execute(sql)
mydb.commit()

sql = "DELETE FROM clusterToTopTerms"
myCursor.execute(sql)
mydb.commit()

sql = "INSERT INTO clusterToTopTerms (top_terms, cluster_id) VALUES (%s, %s)"
myCursor.executemany(sql, tuple_clusterId2TopTerms)
mydb.commit()

sql = "INSERT INTO clusterToDoc (cluster_id, doc_id) VALUES (%s, %s)"
myCursor.executemany(sql, tuple_ClusterId2DocId)
mydb.commit()
#########################################################################################################
