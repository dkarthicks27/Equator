from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from glob import glob
import pickle
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
    label = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4]
    return x, label, y


def svm(vec, feature_names, test_vectors):
    algo = SVC()
    algo.fit(vec, feature_names)
    x = algo.predict(test_vectors)
    print(algo.score())
    # predicted = algo.predict(test_vectors)
    # print(np.mean(predicted == feature_names))


def main():
    tfidf_train, tfidf_features, tfidf_test = tfidf()
    enter = input('Enter 1 for SVM, 2 for Logistic regression: ')
    if enter == 1:
        svm(tfidf_train, tfidf_features, tfidf_test)
    else:
        logisticRegression(tfidf_train, tfidf_features, tfidf_test)


def logisticRegression(vec, feature_names, test_vectors):
    lr = LogisticRegression(n_jobs=1)
    lr.fit(vec, feature_names)
    # print(lr.predict(test_vectors))
    print(lr.score(vec, feature_names))


if __name__ == '__main__':
    main()
