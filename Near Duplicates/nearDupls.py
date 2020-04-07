from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from glob import glob
import os
import pandas as pd

filepath = '/Users/karthickdurai/Equator/OneDoc/*.txt'
file_list = glob(filepath)
train, test = train_test_split(file_list, train_size=0.5)
arr = os.listdir(r'/Users/karthickdurai/Equator/OneDoc/')
labels = arr


def cosineSimilarity(threshold):
    """
    cosine similarity function here is used to find similarity between documents:
    so we first find tfidf of all the  text files
    then we make a pairwise similarity matrix which is then used to determine similarity between vectors
    """
    tfidf = TfidfVectorizer(input='filename', decode_error='ignore', ngram_range=(2, 4))
    x = tfidf.fit_transform(file_list)
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
    operation = input('enter 1: to print the result and 2: to save it as csv: ')
    if operation == 1:
        print(pd.Series(obj))
    elif operation == 2:
        export.to_csv('/Users/karthickdurai/Equator/result.csv')


if __name__ == '__main__':
    cosineSimilarity(0.95)
