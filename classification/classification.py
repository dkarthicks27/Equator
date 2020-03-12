import os
import pandas as pd
import nltk
import glob
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import itertools




path = "/home/eqt2/OneDoc/"
file_paths = glob.glob(path + "*.txt")
files = os.listdir(path)
file_names = []
file_list = []

for file in files:
    file_names.append(file)




labels = ['gas', 'sugar', 'electricity']
from sklearn import preprocessing

le = preprocessing.LabelEncoder()
label = le.fit_transform(labels)
# print(label)
labels_id = []
for (x, y) in itertools.product(label, range(12)):
    labels_id.append(x)

# print(labels_id)
from sklearn.pipeline import Pipeline

# text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
# text_clf.fit_transform()






count_vect = CountVectorizer(input='filename', stop_words='english', encoding='utf-8', decode_error='ignore')
x_train_counts = count_vect.fit_transform(file_paths)





tfIDF_transformer = TfidfTransformer()
x_train_tfidf = tfIDF_transformer.fit_transform(x_train_counts)
# print(x_train_tfidf.shape)
x = pd.DataFrame(x_train_tfidf.toarray())
# print(x)





clf = MultinomialNB().fit(x_train_tfidf, labels_id)
doc = glob.glob('/home/eqt2/10 Documents/*.txt')
x_new_counts = count_vect.transform(doc)
x_new_tfidf = tfIDF_transformer.transform(x_new_counts)

import numpy as np



predicted = clf.predict(x_new_tfidf)
# for (x, y) in zip(doc, predicted):
#    print('%s : %s' % (x, y))


import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='demo',
    password='password'
)

mycursor = mydb.cursor()
mycursor.execute('SHOW DATABASES')

for c in mycursor:
    print(c)