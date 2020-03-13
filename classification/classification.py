import os

import mysql
import pandas as pd
import nltk
import glob
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import itertools
from sklearn import preprocessing


def appendFiles(files, file_names):
    for file in files:
        file_names.append(file)


def createLabelId(labels):
    le = preprocessing.LabelEncoder()
    label = le.fit_transform(labels)
    labels_id = []
    for (x, y) in itertools.product(label, range(12)):
        labels_id.append(x)
    return labels_id


def makePipeLine(text):
    from sklearn.pipeline import Pipeline
    text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
    text_clf.fit_transform(text)


def countVectorizer(file_paths):
    count_vect = CountVectorizer(input='filename', stop_words='english', encoding='utf-8', decode_error='ignore')
    x_train_counts = count_vect.fit_transform(file_paths)
    return x_train_counts


def tfIDF(x_train_counts):
    tfIDF_transformer = TfidfTransformer()
    x_train_tfidf = tfIDF_transformer.fit_transform(x_train_counts)
    # print(x_train_tfidf.shape)
    x = pd.DataFrame(x_train_tfidf.toarray())
    # save = ConnectToSQL()
    # save.saveToDatabase(vector=x)
    # x.drop(x.iloc[:, 1000:], inplace=True, axis=1)
    x.to_csv(r'/home/eqt2/Desktop/csv/vector.csv')
    return x_train_tfidf


def classification(trainVector, labels_id, testVector, doc_id):
    clf = MultinomialNB().fit(trainVector, labels_id)
    import numpy as np
    predicted = clf.predict(testVector)
    # return 'The document ' + str(doc_id) + 'is in the class ' + str(predicted)
    print('The document ' + str(doc_id) + 'is in the class ' + str(predicted))
    # for (x, y) in zip(doc, predicted):
    #    print('%s : %s' % (x, y))


class ConnectToSQL:
    def __init__(self):
        import mysql.connector
        from sqlalchemy import create_engine
        self.mydb = create_engine("mysql+mysqlconnector://root:password@localhost/python")

    def saveToDatabase(self, vector):
        ip = input('enter the table name: ')
        vector.to_sql(name='Vec', con=self.mydb, if_exists='replace')


def main():
    # this is the function where we want the execution to begin:
    # first we will create file_paths which will be used in count vectorizer and tfidf vectorizer
    path = "/home/eqt2/OneDoc/"
    file_paths = glob.glob(path + "*.txt")
    files = os.listdir(path)
    file_names = []
    file_list = []
    appendFiles(file_names=file_names, files=files)  # now we have the filePaths appended so lets create labels
    labels = ['gas', 'sugar', 'electricity']
    labels_id = createLabelId(labels=labels)  # so now we have created labels
    count_vect = countVectorizer(file_paths=file_paths)
    tfidf = tfIDF(count_vect)


if __name__ == '__main__':
    main()
