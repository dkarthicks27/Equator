# here we are going to use lsi and knn to solve classification problem.
# first let us import SVD and LSI

from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import TruncatedSVD
import pickle
from sklearn.model_selection import train_test_split


vec = pickle.load(open("/Users/karthickdurai/Equator/Complete process/vectors.pickle", 'rb'))
train, test = train_test_split(vec, train_size=0.05)
trainLabels = [1, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5]


def classify_lsi():
    lsi = TruncatedSVD(100)
    lsi_train = lsi.fit_transform(train)
    lsi_test = lsi.transform(test)
    knn_lsi = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
    knn_lsi.fit(lsi_train, trainLabels)
    p = knn_lsi.predict(lsi_test)
    # print(p)
    print(knn_lsi.score(lsi_train, trainLabels))


def classify_tfidf():
    knn_tfidf = KNeighborsClassifier(n_neighbors=5, algorithm='auto', metric='euclidean')
    knn_tfidf.fit(train, trainLabels)
    p = knn_tfidf.predict(test)
    print(knn_tfidf.score(train, trainLabels))


if __name__ == '__main__':
    val = int(input("1 for lsi_method\n2 for tfidf_method\n3 to quit: "))
    while val != 3:
        if val == 1:
            classify_lsi()
        elif val == 2:
            classify_tfidf()
        else:
            print("not the right option")
        val = int(input("\nEnter: "))
