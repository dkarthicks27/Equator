from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import time
from glob import glob
import pickle


def tfidf(filePath, n_gram=(1, 3)):
    print('Tfidf initiated\n')
    t_initial = time.time()
    vectorizer = TfidfVectorizer(input='filename', use_idf=True,
                                 stop_words='english',
                                 decode_error='ignore', max_df=0.50, sublinear_tf=True, ngram_range=n_gram,
                                 lowercase=True)
    vectors = vectorizer.fit_transform(filePath)
    print('Model generation and transformation complete')





    svd = TruncatedSVD(n_components=100)
    truncatedVectors = svd.fit_transform(vectors)
    query = [r'/Users/karthickdurai/Equator/OneDoc/117.txt']
    sample_vec = vectorizer.transform(query)
    truncateSample = svd.transform(sample_vec)
    sims = cosine_similarity(truncateSample, truncatedVectors)

    for pos, element in zip(filePath, sims[0]):
        if element >= 0.80:
            print("doc " + str(pos) + " is " + str(element * 100) + "% similar")
    print(f'Time taken to index the documents is {time.time() - t_initial}')
    return vectorizer, vectors


def singularValueD(vectors):
    svd = TruncatedSVD(n_components=100)
    truncatedVectors = svd.fit_transform(vectors)
    return truncatedVectors

def hashingVec(filePath, n_gram=(1, 3)):
    pass


######################################################################################################

if __name__ == '__main__':
    # Construct the argument parser
    files = glob(r'/Users/karthickdurai/Equator/OneDoc/*.txt')

    t1 = time.time()
    print('processing starts....\n')

    vectorizer, vector = tfidf(filePath=files)
    reducedVector = singularValueD(vector)
