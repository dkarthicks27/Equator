import pickle
from pprint import pprint

from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from glob import glob
from sklearn.model_selection import train_test_split


def classify(max_features, threshold, filePath, label):
    trainPath, testPath = train_test_split(filePath, train_size=0.05)
    # print(len(trainPath))
    x = pickle.load(open(r'/Users/karthickdurai/Equator/Complete process/vectors.pickle', 'rb'))
    vectorizer = pickle.load(open(r'/Users/karthickdurai/Equator/Complete process/vectorizer.pickle', 'rb'))
    testVec = vectorizer.transform(trainPath)
    nvb = MultinomialNB()
    nvb.fit(testVec, label)
    result = nvb.predict_proba(x)
    values = {}
    for files, vectors in zip(filePath, result):
        arr = []
        for lab, vecs in zip(label, vectors):
            if vecs >= threshold:
                arr.append(vecs)

        if len(arr) == max_features:
            values[files] = arr

    pprint(values)


path = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')
put = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5]
classify(max_features=2, threshold=0.3, filePath=path, label=put)
