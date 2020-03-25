from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from glob import glob
import pickle
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

filepath = '/Users/karthickdurai/Equator/OneDoc/*.txt'
file_list = glob(filepath)
train, test = train_test_split(file_list, train_size=0.05)


def savePickle():
    array = [1, 2, 3, 4]
    pcfile = open('picklefile', 'ab')
    pickle.dump(array, pcfile)
    pcfile.close()


def loadPickle():
    pcfile = open(r'picklefile', 'rb')
    array = pickle.load(pcfile)
    print(array)
    print(pcfile.read())


def tfidf():
    tfidf = TfidfVectorizer(input='filename', decode_error='ignore')
    x = tfidf.fit_transform(train)
    y = tfidf.transform(test)
    label = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    # return x, label, y
    model = SVC(probability=True)
    # here we are using SVM algorithm
    algo = CalibratedClassifierCV(model)
    algo.fit(x, label)
    # here we fit it with calibrated classifier which calibrates our model to produce accurate data's
    predict = algo.predict(x)
    prob_distribution = algo.predict_proba(y)
    # this is used to find relevance score, as it says how relevant each document is to the labels
    print("below: first element is label 1 probability and label 2 probability:")
    print('Relevance score: ')
    for rows, i in enumerate(prob_distribution, 0):
        print('doc no: ' + str(rows + 1) + ' ' + str(i))
    # print(algo.score(x, label))


def vectorization():
    tfidf = TfidfVectorizer(input='filename', decode_error='ignore')
    x = tfidf.fit_transform(train)
    df = pd.DataFrame(x.toarray())
    df.to_csv(r'file.csv')
    print(df)


def svm(vec, feature_names, test_vectors):
    algo = SVC()
    algo.fit(vec, feature_names)
    x = algo.predict(test_vectors)
    print("svm: ")
    # print('svm score is: ' + str(algo.score(test_vectors, x)))
    # predicted = algo.predict(test_vectors)
    # print(np.mean(predicted == feature_names))


def main():
    tfidf()
    enter = input('Enter 1 for SVM, 2 for Logistic regression: ')
    # if enter == 1:
    # svm(tfidf_train, tfidf_features, tfidf_test)
    # else:
    # logisticRegression(tfidf_train, tfidf_features, tfidf_test)


def logisticRegression(vec, feature_names, test_vectors):
    lr = LogisticRegression(n_jobs=1)
    lr.fit(vec, feature_names)
    # print(lr.predict(test_vectors))
    # print(lr.score(vec, feature_names))


if __name__ == '__main__':
    vectorization()
