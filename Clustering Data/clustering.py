import os
import numpy as np
import pandas as pd
import nltk
import re
import codecs

from nltk.corpus import stopwords
from sklearn import feature_extraction
import mpld3

path = "/home/eqt2/10 Documents/"
files = os.listdir(path)

file_list = []
for file in files:
    with codecs.open(path + file, "r", encoding='utf-8', errors='ignore') as txt:
        file_list.append(txt.read())
# till now i have opened the file

# print(len(file_list)) yes file system exists
# print(file_list[1])




stopWords = stopwords.words('english')
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")

def tokenize_and_stem(text):
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z0-9]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

total_vocab = []
for i in file_list:
    total_vocab.extend(tokenize_and_stem(i))




from sklearn.feature_extraction.text import TfidfVectorizer
tfid_vectorizer = TfidfVectorizer(max_df=0.85, min_df=0.3, stop_words="english", use_idf=True,
                                  tokenizer=tokenize_and_stem, ngram_range=(1,1))
tfidf_matrix = tfid_vectorizer.fit_transform(file_list)
terms = tfid_vectorizer.get_feature_names()




from sklearn.metrics.pairwise import cosine_similarity

dist = 1 - cosine_similarity(tfidf_matrix)



from sklearn.cluster import KMeans

num_clusters = 50
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
#print(km.labels_)
# clusters = pd.DataFrame(km.labels_)
# print(clusters)
print("top terms in cluster: ")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
for i in range(num_clusters):
    print("cluster %d: " % i)
    for ind in order_centroids[i, :4]:
        print('%s' % terms[ind])
    print("")

Y = tfid_vectorizer.transform(["why do i need to send a mail"])
prediction = km.predict(Y)
print(prediction)


#for i in range(len(km.labels_)):
    #if km.labels_[i] == 0:
        #print(i)
