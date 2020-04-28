from sklearn import datasets
import pickle
# from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from glob import glob
import os
from sklearn.metrics.pairwise import cosine_similarity


def delete():
    os.remove("vec_count.joblib")
    print("File Removed!")


def vectorize():
    vec = TfidfVectorizer(input="filename", decode_error="ignore")
    k = vec.fit_transform(file)
    with open('vec_count.pickle', 'ab') as y:
        pickle.dump(vec, y)
    return k


#    vec = pickle.load(open('vec_count.pickle', 'rb'))
#    x = vec.transform(['/Users/karthickdurai/Equator/OneDoc/300.txt'])
#    result = cosine_similarity(x, k)
#    print(result)


def transform(k):
    vec = pickle.load(open('vec_count.pickle', 'rb'))
    x = vec.transform(['/Users/karthickdurai/Equator/OneDoc/300.txt'])
    result = cosine_similarity(x, k)
    print(result)


if __name__ == '__main__':

    d = input("do you want to delete the file: ")
    if d == 'y':
        delete()

    file = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')

    fitted = vectorize()
    transform(k=fitted)
