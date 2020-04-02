from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from glob import glob

filepath = '/Users/karthickdurai/Equator/OneDoc/*.txt'
file_list = glob(filepath)
train, test = train_test_split(file_list, train_size=0.5)


def cosineSimilarity(threshold):
    """
    cosine similarity function here is used to find similarity between documents:
    so we first find tfidf of all the  text files
    then we make a pairwise similarity matrix which is then used to determine similarity between vectors
    """
    tfidf = TfidfVectorizer(input='filename', decode_error='ignore')
    x = tfidf.fit_transform(file_list)
    similarity = cosine_similarity(x)
    """
    now here we are printing all the similar documents respect to each document according to threshold
    """
    for line, val in enumerate(similarity, 1):
        for position, items in enumerate(val, 1):
            # print("\ndocuments similar to document " + str(line) + " with: ")
            if (line != position) and (items >= threshold):
                print("doc " + str(position) + " is " + str(items * 100) + " similar to doc " + str(line))


if __name__ == '__main__':
    cosineSimilarity(0.95)